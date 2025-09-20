import jwt
from flask import request, g
from functools import wraps

from configs import AuthConfig
from configs.ServerConfig import logger

def jwt_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{g.request_id} - checking jwt token")
        auth_header = request.headers.get("Authorization", None)

        if not auth_header or not auth_header.startswith("Bearer "):
            logger.error(f"{g.request_id} - jwt token is absent")
            g.response_code = '0401'
            return {"code": "0401", "description": "Authorization header missing or invalid"}, 401

        token = auth_header.split(" ")[1]

        try:
            decode = jwt.decode(token, AuthConfig.jwt_secret, algorithms=[AuthConfig.jwt_algorithm])
            g.user_id = decode["user_id"]
            logger.debug(f"{g.request_id} - jwt token is valid")
            logger.info(f"{g.request_id} - endpoint requested by user_id: '{g.user_id}'")
        except jwt.ExpiredSignatureError:
            logger.error(f"{g.request_id} - jwt token has expired")
            g.response_code = '0401'
            return {"code": "0401", "description": "token has expired"}, 401
        except jwt.InvalidTokenError:
            logger.error(f"{g.request_id} - jwt token is invalid")
            g.response_code = '0401'
            return {"code": "0401", "description": "invalid jwt token"}, 401

        return func(*args, **kwargs)

    return wrapper