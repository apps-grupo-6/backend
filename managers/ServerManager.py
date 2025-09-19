from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def create_request_log(final_response, conn, cursor, user_id, method, endpoint, code, execution_time, request_id):
    try:
        query = """
            INSERT INTO requests (id, user_id, method, endpoint, code, execution_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (request_id, user_id, method, endpoint, code, execution_time)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the log")
        final_response["ok"] = False

    return final_response