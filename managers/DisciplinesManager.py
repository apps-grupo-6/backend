from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
def does_disciplines_exist(final_response, conn, cursor, discipline_id, request_id):
    try:
        query = """
            SELECT 1
            FROM disciplines
            WHERE id = %s
            LIMIT 1;
        """
        values = (discipline_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if discipline exists")
        final_response["ok"] = False

    return final_response