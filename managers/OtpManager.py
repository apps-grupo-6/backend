from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
def check_if_user_has_active_otp(final_response, conn, cursor, user_id, type, request_id):
    try:
        query = """
            SELECT expires_at, token as otp_token
            FROM otp_tokens
            WHERE 
                user_id = %s
                AND type = %s
            LIMIT 1;
        """
        values = (user_id, type)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if the user has an otp_token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def save_otp(final_response, conn, cursor, user_id, otp_token, type, request_id):
    try:
        query = """
            INSERT INTO otp_tokens (user_id, token, type, expires_at)
            VALUES (%s, %s, %s, NOW() + INTERVAL '15 minutes')
            ON CONFLICT (user_id, type)
            DO UPDATE SET
                token = EXCLUDED.token,
                expires_at = EXCLUDED.expires_at;
        """
        values = (user_id, otp_token, type)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating or updating the otp_token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def delete_otp(final_response, conn, cursor, user_id, otp_token, type, request_id):
    try:
        query = """
            DELETE FROM otp_tokens
            WHERE 
                user_id = %s 
                AND token = %s
                AND type = %s
        """
        values = (user_id, otp_token, type)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while deleting the otp_token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def check_otp_token_by_username(final_response, conn, cursor, username, otp_token, type, request_id):
    try:
        query = """
            SELECT ot.user_id, ot.expires_at, ot.token
            FROM otp_tokens ot
            JOIN users u ON u.id = ot.user_id
            WHERE 
                u.username = %s
                AND ot.token = %s
                AND ot.type = %s
            LIMIT 1;
        """
        values = (username, otp_token, type)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking otp_token by username")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_user_by_verification_code(final_response, conn, cursor, username, verification_code, request_id):
    try:
        query = """
            SELECT u.id, u.username, u.verification_expires_at, ui.first_name, ui.last_name, ui.contact_email
            FROM users u
            JOIN user_information ui ON ui.user_id = u.id
            WHERE u.username = %s AND u.verification_token = %s AND u.email_verified = FALSE
            LIMIT 1
        """
        cursor.execute(query, (username, verification_code))
        final_response["data"] = cursor.fetchone()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while getting user by verification code: {e}")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def mark_user_as_verified(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            UPDATE user_controls 
            SET email_verified = TRUE,
                email_verified_at = NOW()
            WHERE user_id = %s
        """
        values = (user_id,)

        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while marking user as verified: {e}")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def check_otp_token_by_user_id(final_response, conn, cursor, user_id, otp_token, type, request_id):
    try:
        query = """
            SELECT expires_at
            FROM otp_tokens ot
            WHERE 
                ot.user_id = %s
                AND ot.token = %s
                AND ot.type = %s
            LIMIT 1;
        """
        values = (user_id, otp_token, type)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking otp_token by user_id")
        final_response["ok"] = False

    return final_response