from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def get_username_info(final_response, conn, cursor, username, request_id):
    try:
        query = """
            SELECT 
                id as user_id, 
                password
            FROM users
            WHERE username = %s
            LIMIT 1;
        """
        values = (username,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while registering the user")
        final_response["ok"] = False

    return final_response

@with_db_connection
def check_otp_token(final_response, conn, cursor, user_id, otp_token, request_id):
    try:
        query = """
            SELECT expires_at
            FROM otp_tokens
            WHERE 
                user_id = %s
                AND token = %s
            LIMIT 1;
        """
        values = (user_id, otp_token)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while registering the user")
        final_response["ok"] = False

    return final_response
