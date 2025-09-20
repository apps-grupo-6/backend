import awsgi
from flask import Flask, g, jsonify, request
from datetime import datetime

from configs.ServerConfig import run_check, logger
from controllers import AuthController, UsersController, OtpController, ClassesController, LocationsController
from connectors import ServerConnector
from repositories import ServerRepository

app = Flask(__name__)

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
    g.response_code = ""
    g.description_code_map = {}
    g.begin_time = datetime.now()
    g.user_id = -1
    g.endpoint = ""
    g.method = ""

    logger.info(f"{g.request_id} - begin")
    logger.info(f"{g.request_id} - request body: {request.get_data(as_text=True)}")

@app.after_request
def after_request(response):
    if g.send_email_data:
        ServerConnector.send_email(email=g.send_email_data, request_id=g.request_id)

    if response.content_type == 'application/json':
        original_data = response.get_json()
        original_data["request_id"] = g.request_id

        if not g.response_code == "0401": # if not related to jwt token, retrieve all related information
            response_data = g.description_code_map[g.response_code]
            original_data["code"] = g.response_code
            original_data["description"] = response_data[0]
            response.status_code = response_data[1]

        response.set_data(jsonify(original_data).get_data())

    g.end_time = datetime.now() - g.begin_time
    end_time_seconds = g.end_time.total_seconds()

    if g.user_id != -1:
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
    return {"error": "not found"}, 404

@app.errorhandler(405)
def internal_error(error):
    return {"error": "check URI and request body"}, 405

@app.errorhandler(415)
def internal_error(error):
    return {"error": "request body is empty"}, 415

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == "__main__":
    for check in run_check:
        controller = check.split("=")
        controller_name = controller[0]
        controller_enabled = controller[1]

        if controller_enabled == "1":
            logger.debug(msg=f"{controller_name} is enabled")
            bp = CONTROLLERS_BP[controller_name]
            app.register_blueprint(bp, url_prefix=f"/api/{controller_name}")

    logger.info("Starting backend...")
    app.run(debug=True, host='0.0.0.0', port=5000)