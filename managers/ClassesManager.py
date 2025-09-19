from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def check_if_duplicated(final_response, conn, cursor, professor_id, location_id, discipline_id, request_id):
    try:
        query = """
            SELECT scheduled_at, ended_at
            FROM classes
            WHERE 
                professor_id = %s
                AND location_id = %s
                AND discipline_id = %s
            LIMIT 1;
        """
        values = (professor_id, location_id, discipline_id)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if the class is repeated")
        final_response["ok"] = False

    return final_response

@with_db_connection
def create_class(final_response, conn, cursor, professor_id, location_id, discipline_id, scheduled_at, max_participants,
                 qr, request_id):
    try:
        query = """
            INSERT INTO classes (professor_id, location_id, discipline_id, scheduled_at, max_participants, qr)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (professor_id, location_id, discipline_id, scheduled_at, max_participants, qr)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def does_class_exist(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT 1
            FROM classes
            WHERE id = %s
            LIMIT 1;
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if class exists")
        final_response["ok"] = False

    return final_response

@with_db_connection
def finish_class(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            UPDATE classes
            SET ended_at = NOW()
            WHERE id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to finish this class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def update_class(final_response, conn, cursor, update_columns, update_values, request_id):
    try:
        query = f"""
            UPDATE classes
            SET {update_columns}
            WHERE id = %s
        """
        values = update_values

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to finish this class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def get_class_information(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT professor_id, location_id, discipline_id, scheduled_at, ended_at, max_participants, qr
            FROM classes
            WHERE id = %s
            LIMIT 1;
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to obtain class information")
        final_response["ok"] = False

    return final_response