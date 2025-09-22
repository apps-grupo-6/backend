from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
def register_account(final_response, conn, cursor, username, password, first_name,
                     last_name, telephone, email, request_id):
    try:
        procedure_call = """
            SELECT register_account(%s, %s, %s, %s, %s, %s)
        """
        values = (username, password, first_name, last_name, telephone, email)

        cursor.execute(procedure_call, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while registering the user")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_user_information(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT contact_email, first_name, last_name, telephone
            FROM user_information
            WHERE user_id = %s
            LIMIT 1;
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to obtain contact email")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def does_user_exist(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT 1
            FROM users
            WHERE id = %s
            LIMIT 1;
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if user exists")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def does_username_exist(final_response, conn, cursor, username, request_id):
    try:
        query = """
            SELECT id
            FROM users
            WHERE username = %s
            LIMIT 1;
        """
        values = (username,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if username exists")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def update_user(final_response, conn, cursor, update_columns, update_values, request_id):
    try:
        query = f"""
            UPDATE user_information
            SET updated_at = NOW(),
                {update_columns}
            WHERE user_id = %s
        """
        values = tuple(update_values)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to update user information")
        final_response["ok"] = False

    return final_response