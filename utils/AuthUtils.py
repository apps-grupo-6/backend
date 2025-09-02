import jwt
from flask import request
from functools import wraps

from configs import AuthConfig

def jwt_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)

        if not auth_header or not auth_header.startswith("Bearer "):
            return {"code": "0401", "description": "Authorization header missing or invalid"}, 401

        token = auth_header.split(" ")[1]

        try:
            jwt.decode(token, AuthConfig.jwt_secret, algorithms=[AuthConfig.jwt_algorithm])
        except jwt.ExpiredSignatureError:
            return {"code": "0401", "description": "token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"code": "0401", "description": "invalid jwt token"}, 401

        return func(*args, **kwargs)

    return wrapper