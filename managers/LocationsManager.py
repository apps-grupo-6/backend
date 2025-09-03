from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def does_location_exist(final_response, conn, cursor, location_id, request_id):
    try:
        query = """
            SELECT 1
            FROM locations
            WHERE id = %s
            LIMIT 1;
        """
        values = (location_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if location exists")
        final_response["ok"] = False

    return final_response