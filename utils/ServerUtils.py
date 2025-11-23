import importlib, re
from functools import wraps

from flask import g, request
from configs.ServerConfig import logger

from connectors import ServerConnector
from managers import NotificationsManager
from repositories import ServerRepository
from templates import ServerTemplates, UserTemplate

USERS_DATA = {}
BACKEND_DEVELOPERS = {}
DESCRIPTIONS_CODE_MAPS = {}
CONTROLLERS_BP = {}

def configure_request(rule):
    global DESCRIPTIONS_CODE_MAPS
    bp_name, func_name = g.endpoint.split(".", 1)
    config_module_name = f"configs.{bp_name.capitalize()}Config"
    endpoint_code_map = f"{func_name}_code_map"

    try:
        if config_module_name not in DESCRIPTIONS_CODE_MAPS:
            DESCRIPTIONS_CODE_MAPS[config_module_name] = importlib.import_module(config_module_name)
    except ModuleNotFoundError:
        logger.exception(f"{g.request_id} - config module '{config_module_name}' not found")

    try:
        config_module = DESCRIPTIONS_CODE_MAPS[config_module_name]
        g.description_code_map = getattr(config_module, endpoint_code_map)
    except AttributeError:
        logger.exception(f"{g.request_id} - endpoint config code map '{endpoint_code_map}' not found")

    normalized = re.sub(r"<[^:<>]+:([^<>]+)>", r"<\1>", rule.rule).replace("/api", "")
    g.endpoint = normalized
    g.endpoint_id_list = []

    for key, value in request.view_args.items():
        g.endpoint_id_list.append(str(value))

def controller_bp(controller_name):
    global CONTROLLERS_BP

    module_name = f"controllers.{controller_name.capitalize()}Controller"

    if controller_name in CONTROLLERS_BP:
        return CONTROLLERS_BP[controller_name]

    try:
        module = importlib.import_module(module_name)
        bp = getattr(module, "bp")
        CONTROLLERS_BP[controller_name] = bp
    except ModuleNotFoundError:
        raise RuntimeError(f"Controller module not found: {module_name}")
    except AttributeError:
        raise RuntimeError(f"Controller module {module_name} has no 'bp' attribute")
    return bp

def set_final_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        final_response = {
            "ok": True,
            "data": {},
            "error": False
        }

        result = func(*args, **kwargs)
        if result["flag"] == -1: # database error
            final_response["ok"] = False
            g.response_code = kwargs["errors_code_map"]["database_error_code"]
            final_response["error"] = True
        elif result["flag"] == 0: # no results found or specific checks
            g.response_code = kwargs["errors_code_map"]["invalid_data_error_code"]
            final_response["error"] = True
            final_response["data"] = result["data"] if "data" in result else {} # in case some data were required to check
        else: # flag == 1 -> results were found or action was done properly
            final_response["data"] = result["data"] if "data" in result else {}
        return final_response
    return wrapper

def get_users():
    global USERS_DATA, BACKEND_DEVELOPERS

    users_data = ServerRepository.get_users()
    USERS_DATA = users_data
    temp = {}

    for user in users_data["data"]:
        user_information = users_data["data"][user]
        user_roles = user_information["roles"]

        if "BACKEND DEVELOPER" in user_roles:
            user_contact = user_information["information"]
            temp[user] = {
                "user_email": user_contact["contact_email"],
                "user_firstname": user_contact["first_name"],
                "user_lastname": user_contact["last_name"]
            }

    BACKEND_DEVELOPERS = temp

def send_email_alert_backend():
    endpoint = g.endpoint
    method = g.method
    request_id = g.request_id
    response_code = g.response_code
    description = g.alert_description

    email = {
        "subject": "ALERTA DE SEGURIDAD",
        "endpoint": endpoint,
        "method": method,
        "request_id": request_id,
        "response_code": response_code,
        "html_content": ServerTemplates.render_alert_email(description=description,
                                                           endpoint=endpoint,
                                                           method=method,
                                                           request_id=request_id,
                                                           response_code=response_code)
    }

    logger.critical(f"{g.request_id} - sending alert email and notifying all backend developers...")
    for developer in BACKEND_DEVELOPERS:
        backend_developer = BACKEND_DEVELOPERS[developer]
        email["user_email"] = backend_developer["user_email"]
        email["user_firstname"] = backend_developer["user_firstname"]
        email["user_lastname"] = backend_developer["user_lastname"]

        ServerConnector.send_email(email=email, request_id=g.request_id)

def send_email_account_blocked(user_data):
    user_information = user_data["information"]
    username = user_information["username"]
    contact_email = user_information["contact_email"]
    firstname  = user_information["first_name"]
    lastname = user_information["last_name"]

    email = {
        "subject": "Tu cuenta ha sido bloqueada",
        "user_email": contact_email,
        "user_firstname": firstname,
        "user_lastname": lastname,
        "html_content": UserTemplate.render_banned_account_email(first_name=firstname,
                                                                 last_name=lastname,
                                                                 username=username)
    }

    logger.info(f"{g.request_id} - notifying user being banned...")
    ServerConnector.send_email(email=email, request_id=g.request_id)

def send_push_notification_account_blocked(user_data):
    final_response = {
        "data": {
            "title": "",
            "body": "",
            "categoryId": "",
            "data": {}
        }
    }

    user_information = user_data["information"]
    logger.info(f"{g.request_id} - generating ban push notification for user_id '{g.user_id}'...")

    final_response["data"]["title"] = f"Tu cuenta ha sido bloqueada"
    final_response["data"]["body"] = f"La cuenta {user_information['username']} ha sido bloqueada automáticamente por motivos internos de seguridad. Si crees que es un error, contacta al soporte."

    users_to_notify = NotificationsManager.get_user_token(user_id=g.user_id, request_id=g.request_id)
    g.send_push_notification_data = final_response["data"]
    g.send_push_notification_users_token = [users_to_notify["data"]["expo_push_token"]]

    logger.info(users_to_notify)
