from flask import g
from functools import wraps

from configs.ServerConfig import logger
from connectors import ServerConnector
from repositories import ServerRepository
from templates import ServerTemplates, UserTemplate

USERS_DATA = {}
BACKEND_DEVELOPERS = {}

def configure_request(description_code_map, method="", endpoint=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            g.method = method
            g.description_code_map = description_code_map

            final_endpoint = endpoint

            if endpoint and "<id>" in endpoint:
                id = str(kwargs['id'])
                g.endpoint_id_list.append(id)
                final_endpoint = endpoint.replace("<id>", id)

            g.endpoint = f"/{func.__module__.split('.')[-1].replace('Controller', '').lower()}/{final_endpoint}"
            return func(*args, **kwargs)
        return wrapper
    return decorator

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
        elif result["flag"] == 0: # no results found
            g.response_code = kwargs["errors_code_map"]["invalid_data_error_code"]
            final_response["error"] = True
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

    logger.debug(f"{g.request_id} - sending email: {email}")
    logger.info(f"{g.request_id} - notifying all backend developers...")
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
        "subject": "Tu cuenta ha sido bloqueada en Excuses 404",
        "user_email": contact_email,
        "user_firstname": firstname,
        "user_lastname": lastname,
        "html_content": UserTemplate.render_banned_account_email(first_name=firstname,
                                                                 last_name=lastname,
                                                                 username=username)
    }

    logger.debug(f"{g.request_id} - sending email: {email}")
    ServerConnector.send_email(email=email, request_id=g.request_id)