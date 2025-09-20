from flask import g
from functools import wraps

def configure_request(description_code_map, method="", endpoint=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            g.method = method
            g.description_code_map = description_code_map

            final_endpoint = endpoint
            if endpoint and "<id>" in endpoint:
                final_endpoint = endpoint.replace("<id>", str(kwargs['id']))

            g.endpoint = f"/{func.__module__.split(".")[-1].replace("Controller", "").lower()}/{final_endpoint}"
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
