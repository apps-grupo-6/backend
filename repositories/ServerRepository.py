from configs.ServerConfig import logger
from managers import ServerManager

def create_request_log(request_id, user_id, method, endpoint, code, execution_time):
    logger.info(f"{request_id} - saving request log...")

    created = ServerManager.create_request_log(request_id=request_id,
                                               user_id=user_id,
                                               method=method,
                                               endpoint=endpoint,
                                               code=code,
                                               execution_time=execution_time)
    if not created["ok"]:
        logger.critical(f"{request_id} - an error occurred while creating the request log")
        logger.info(f"request data: {request_id=} | {user_id=} | {method=} | {endpoint=} | {code=} | {execution_time=}")
    else:
        logger.debug(f"{request_id} - request log created successfully")

def get_users():
    logger.info("retrieving all users information...")

    users = ServerManager.get_users()
    if not users["ok"]:
        logger.critical("an error occurred when retrieving users")

    logger.debug("all users information retrieved successfully")
    return users["data"]

def set_user_as_suspect(user_id, request_id):
    logger.info(f"{request_id} - setting user_id '{user_id}' as suspect...")

    set_user = ServerManager.set_user_as_suspect(user_id=user_id, request_id=request_id)
    if not set_user["ok"]:
        logger.critical(f"{request_id} - an error occurred while setting the user as suspect")
    else:
        logger.debug(f"{request_id} - user set as suspect successfully")

def set_user_as_banned(user_id, request_id):
    logger.info(f"{request_id} - banning user_id '{user_id}'...")

    set_user = ServerManager.set_user_as_banned(user_id=user_id, request_id=request_id)
    if not set_user["ok"]:
        logger.critical(f"{request_id} - an error occurred while trying to ban this user")
    else:
        logger.debug(f"{request_id} - user banned successfully")

def delete_expired_otp_tokens():
    logger.info("trying to delete all expired otp_tokens...")

    deleted = ServerManager.delete_expired_otp_tokens()
    if not deleted["ok"]:
        logger.critical("an error occurred when trying to delete expired otp_tokens")
    else:
        rows_affected = deleted['data']

        if rows_affected:
            logger.debug(f"{rows_affected} otp_tokens were deleted successfully")
        else:
            logger.debug("all otp_tokens in our database are active")

def reset_force_disconnect(user_id, request_id):
    logger.info(f"{request_id} - resetting force disconnect...")

    reset_disconnect = ServerManager.reset_user_force_disconnect(user_id=user_id, request_id=request_id)
    if not reset_disconnect["ok"]:
        logger.critical(f"{request_id} - an error occurred while trying to reset force disconnect this user")
    else:
        logger.debug(f"{request_id} - forced disconnect flag was rested successfully")