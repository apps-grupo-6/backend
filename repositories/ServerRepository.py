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
        logger.critical(f"{request_id} - an error occurred while creating the request log:")
        logger.info(f"request data: {request_id=} | {user_id=} | {method=} | {endpoint=} | {code=} | {execution_time=}")
    else:
        logger.debug(f"{request_id} - request log created successfully")