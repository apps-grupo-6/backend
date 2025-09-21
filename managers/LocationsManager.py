from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
def create_location(final_response, conn, cursor, owner_id, country_code, city, address, request_id):
    try:
        query = """
            INSERT INTO locations (owner_id, country_code, city, address, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        values = (owner_id, country_code, city, address)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the location")
        final_response["ok"] = False

    return final_response