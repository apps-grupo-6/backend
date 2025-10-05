from flask import Flask, g, jsonify, request
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from configs.ServerConfig import run_check, logger, special_errors_code_map
from controllers import AuthController, UsersController, OtpController, ClassesController, LocationsController
from connectors import ServerConnector
from repositories import ServerRepository
from utils import ServerUtils

app = Flask(__name__)
app.url_map.strict_slashes = False

CONTROLLERS_BP = {
    "auth": AuthController.bp,
    "users": UsersController.bp,
    "otp": OtpController.bp,
    "classes": ClassesController.bp,
    "locations": LocationsController.bp
}

@app.before_request
def before_request():
    g.request_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    g.send_email_data = {}
    g.alert_description = ""
    g.response_code = ""
    g.description_code_map = {}
    g.begin_time = datetime.now()
    g.user_id = -1
    g.user_data = {}
    g.endpoint = ""
    g.method = ""
    g.endpoint_id_list = []

    logger.info(f"{g.request_id} - begin")
    if request.method in ['POST', 'PUT'] and request.is_json:
        logger.info(f"{g.request_id} - request body: {request.json}")
    else:
        logger.info(f"{g.request_id} - request method: {request.method}")

@app.after_request
def after_request(response):
    if g.send_email_data:
        ServerConnector.send_email(email=g.send_email_data, request_id=g.request_id)

    if g.alert_description:
        if g.response_code == "9999" and g.user_data:#if there was a security breach amd user data was retrieved from cache or exists in our database at least
            if g.user_data["suspect"]:
                ServerRepository.set_user_as_banned(user_id=g.user_id, request_id=g.request_id)
                ServerUtils.send_email_account_blocked(g.user_data)
            else:
                ServerRepository.set_user_as_suspect(user_id=g.user_id, request_id=g.request_id)

        ServerUtils.get_users() # forces to reload users cache to update user status if banned o flagged as suspect
        ServerUtils.send_email_alert_backend() # notifies backend developers to check this alert

    if response.content_type == 'application/json':
        original_data = response.get_json()
        original_data["request_id"] = g.request_id

        if g.response_code:
            # 0401 = jwt token errors
            # 0403 = user role cant use the required endpoint with this method
            if not g.response_code in ('0401', '0403'): # if not related to any login error, retrieve all related information
                if g.response_code in special_errors_code_map:
                    description = "the request could not be processed"
                    status_code = 500
                else:
                    response_data = g.description_code_map[g.response_code]
                    description = response_data[0]
                    status_code = response_data[1]

                original_data["code"] = g.response_code
                original_data["description"] = description
                response.status_code = status_code

        response.set_data(jsonify(original_data).get_data())

    g.end_time = datetime.now() - g.begin_time
    end_time_seconds = g.end_time.total_seconds()

    ServerRepository.create_request_log(request_id=g.request_id,
                                        endpoint=g.endpoint,
                                        method=g.method,
                                        code=g.response_code,
                                        user_id=g.user_id,
                                        execution_time=end_time_seconds)

    logger.info(f"{g.request_id} - ended after {end_time_seconds} seconds")
    return response

@app.errorhandler(404)
def not_found(error):
    return {"error": "endpoint not found"}, 404

@app.errorhandler(405)
def internal_error(error):
    return {"error": "check URI and request body"}, 405

@app.errorhandler(415)
def internal_error(error):
    return {"error": "request body is empty"}, 415

def awake_crons():
    crons = {
        "get_users": {
            "function": ServerUtils.get_users,
            "minutes": 1
        }
    }
    scheduler = BackgroundScheduler()

    for cron in crons:
        actual_cron = crons[cron]
        function = actual_cron["function"]

        logger.debug(f"Executing required cron '{cron}' to retrieve its data...")
        function()

        logger.debug(f"Programming cron: {cron} to execute each {actual_cron['minutes']} minutes...")
        #scheduler.add_job(function, "interval", minutes=actual_cron["minutes"])

    scheduler.start()
    logger.info(f"Awaken {len(crons)} crons")


for check in run_check:
    controller_name, controller_enabled = check.split("=")

    if controller_enabled == "1":
        logger.debug(msg=f"{controller_name} is enabled")
        bp = CONTROLLERS_BP[controller_name]
        app.register_blueprint(bp, url_prefix=f"/api/{controller_name}")

awake_crons()

if __name__ == "__main__":
    logger.info("Starting backend...")
    app.run(debug=True, host='0.0.0.0', port=5000)
