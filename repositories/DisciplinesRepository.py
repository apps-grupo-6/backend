from managers import DisciplinesManager
from configs.ServerConfig import logger
from utils import ServerUtils


@ServerUtils.set_final_response
def check_if_discipline_exists(discipline_id, request_id, errors_code_map):
    logger.info(f"{request_id} - checking if discipline_id '{discipline_id}' exists...")
    discipline_exists = DisciplinesManager.does_disciplines_exist(discipline_id=discipline_id, request_id=request_id)

    if not discipline_exists["ok"]:
        logger.critical(f"{request_id} - an error occurred while checking")
        return {"flag": -1}

    if not discipline_exists["data"]:
        logger.error(f"{request_id} - invalid discipline_id")
        return {"flag": 0}

    logger.debug(f"{request_id} - discipline exists")
    return {"flag": 1, "data": discipline_exists['data']}