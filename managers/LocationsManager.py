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
def create_location(final_response, conn, cursor, owner_id, country_code, city, address, name, request_id):
    try:
        query = """
            INSERT INTO locations (owner_id, country_code, city, address, name, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        values = (owner_id, country_code, city, address, name)

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
                d.name AS discipline_name,
                ui.first_name || ' ' || ui.last_name AS professor_name,
                l.name AS gym_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD HH24:MI:SS') as class_scheduled_at,
                c.max_participants AS class_max_participants
            FROM locations l
            JOIN classes c ON l.id = c.location_id
            JOIN user_information ui ON ui.user_id = c.professor_id 
            JOIN disciplines d ON d.id = c.discipline_id
        """

        cursor.execute(query)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to retrieve all locations")
        final_response["ok"] = False

    return final_response