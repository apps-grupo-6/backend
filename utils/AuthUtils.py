import jwt, datetime
from flask import request, g
from functools import wraps

from configs import AuthConfig
from configs.ServerConfig import logger
from repositories import AuthRepository
from utils import ServerUtils

def validate_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{g.request_id} - checking jwt token")
        auth_header = request.headers.get("Authorization", None)

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.error(f"{g.request_id} - jwt token is absent")
            g.response_code = '0401'
            return {"code": "0401", "description": "Authorization header missing or invalid"}, 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, AuthConfig.jwt_secret, algorithms=[AuthConfig.jwt_algorithm])
            user_id = decoded["user_id"] if "data" not in decoded else decoded["data"]["user_id"]
            logger.debug(f"{g.request_id} - jwt token is valid")

            logger.info(f"{g.request_id} - endpoint requested by user_id: '{user_id}'")

            logger.info(f"{g.request_id} - checking if user is cached...")
            str_user_id = str(user_id)
            if not str_user_id in ServerUtils.USERS_DATA["data"]: # maybe user registered between retrieving users cron execution
                logger.info(f"{g.request_id} - checking if user_id '{user_id}' exists our database...")
                exists = AuthRepository.check_if_user_exists(user_id=user_id, request_id=g.request_id)

                if not exists["ok"]:
                    logger.critical(f"{g.request_id} - an error occurred while checking")
                    g.response_code = '-1'
                    return {"code": "0500", "description": "the request could not be processed"}, 500

                if not exists["data"]:
                    g.alert_description = f"user_id '{user_id}' tried to login with a valid jwt token but this user_id is not registered in our database"
                    logger.critical(f"{g.request_id} - [SECURITY BREACH] {g.alert_description}")
                    g.response_code = '9999'
                    return {"code": "0501", "description": "the request could not be processed"}, 500

                data = exists["data"]
            else:
                data = ServerUtils.USERS_DATA["data"]

            user_data = data[str_user_id]
            logger.debug(f"{g.request_id} - user_id exists")
            g.user_id = user_id
            g.user_data = user_data

            if user_data["banned"]: #if user was banned
                logger.error(f"{g.request_id} - user_id is banned")
                g.response_code = '9998'
                return {"code": "0403", "description": "the request could not be processed due to user_id is banned"}, 403

            if user_data["suspect"]: #if user was flagged as suspect
                logger.warning(f"{g.request_id} - user_id '{user_id}' was flagged as suspect")

            if str_user_id not in ServerUtils.BACKEND_DEVELOPERS:
                user_permissions = user_data["permissions"]
                check_endpoint = f"{g.method}-{g.endpoint}"

                if g.endpoint_id_list:
                    for parameter_id in g.endpoint_id_list:
                        check_endpoint = check_endpoint.replace(parameter_id, "<id>", 1)

                if check_endpoint[-1] == "/":
                    check_endpoint = check_endpoint[:-1]

                logger.debug(f"{g.request_id} - the user is trying to use endpoint: [{g.method}] {g.endpoint}")
                if check_endpoint not in user_permissions:
                    logger.error(f"{g.request_id} - user_id '{user_id}' cannot use this endpoint")
                    g.response_code = "9999"
                    g.alert_description = f"user_id '{user_id}' tried to use an endpoint '{check_endpoint}' but its role does not allow it."
                    return {"code": "0403", "description": "you are not allowed to use this function"}, 403
                else:
                    logger.debug(f"{g.request_id} - user_id '{user_id}' can use this endpoint")
            else:
                logger.debug(f"this request was done by a backend developer with the user_id '{user_id}'")

        except jwt.ExpiredSignatureError:
            logger.error(f"{g.request_id} - jwt token has expired")
            g.response_code = '0401'
            return {"code": "0401", "description": "jwt token has expired"}, 401
        except jwt.InvalidTokenError:
            logger.error(f"{g.request_id} - jwt token is invalid")
            g.response_code = '0401'
            return {"code": "0401", "description": "invalid jwt token"}, 401

        return func(*args, **kwargs)

    return wrapper

def check_jwt_token(jwt_token):
    final_response = {
        "data": {},
        "error": True,
        "error_code": -1
    }

    if jwt_token.startswith("Bearer"):
        jwt_token = jwt_token.split(" ")[1]

    try:
        jwt.decode(jwt_token, AuthConfig.jwt_secret, algorithms=[AuthConfig.jwt_algorithm])
        final_response["error_code"] = 0
    except jwt.ExpiredSignatureError:
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        final_response["data"] = decoded
        final_response["error"] = False
    except jwt.InvalidTokenError:
        final_response["error_code"] = 1

    return final_response

def generate_jwt_token(user_id, request_id):
    logger.info(f"{request_id} - generating jwt token...")
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)
    logger.debug(f"{request_id} - jwt token generated successfully")
    return token