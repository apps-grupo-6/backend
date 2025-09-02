from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def check_otp(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT expires_at
            FROM otp_tokens
            WHERE user_id = %s
            LIMIT 1;
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if the user has an otp_token")
        final_response["ok"] = False

    return final_response

@with_db_connection
def create_otp(final_response, conn, cursor, user_id, otp_token, request_id):
    try:
        query = """
            INSERT INTO otp_tokens (user_id, token, expires_at)
            VALUES (%s, %s, NOW() + INTERVAL '15 minutes')
            ON CONFLICT (user_id)
            DO UPDATE SET
                token = EXCLUDED.token,
                expires_at = EXCLUDED.expires_at;
        """
        values = (user_id, otp_token)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating or updating the otp_token")
        final_response["ok"] = False

    return final_response