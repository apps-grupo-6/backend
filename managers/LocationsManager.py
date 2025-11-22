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
def create_location(final_response, conn, cursor, owner_id, country_code, city, address, name, lat, lng, request_id):
    try:
        query = """
            INSERT INTO locations (owner_id, country_code, city, address, name, lat, lng, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        values = (owner_id, country_code, city, address, name, lat, lng)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the location")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_all_locations(final_response, conn, cursor, request_id):
    try:
        query = """
            SELECT 
                ui.first_name || ' ' || ui.last_name AS owner_name,
                l.name AS gym_name,
                l.lat AS gym_latitude,
                l.lng AS gym_longitude,
                l.address AS gym_address,
                l.city AS gym_city
            FROM locations l
            JOIN user_information ui ON ui.user_id = l.owner_id 
        """

        cursor.execute(query)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to retrieve all locations")
        final_response["ok"] = False

    return final_response