from configs.ServerConfig import logger
from utils import DatabaseUtils
import datetime
import random

@DatabaseUtils.with_db_connection
def register_account(final_response, conn, cursor, username, password, first_name,
                     last_name, telephone, email, verification_token, verification_expires_at, request_id):
    try:
        new_user_id = f"{int(datetime.datetime.now().timestamp())}{random.randint(100000, 999999)}"
        
        user_query = """
            INSERT INTO users (id, username, password, email_verified, verification_token, verification_expires_at, created_at, updated_at)
            VALUES (%s, %s, %s, FALSE, %s, %s, NOW(), NOW())
        """
        cursor.execute(user_query, (new_user_id, username, password, verification_token, verification_expires_at))
        
        info_query = """
            INSERT INTO user_information (user_id, first_name, last_name, contact_email, telephone, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(info_query, (new_user_id, first_name, last_name, email, telephone))
        
        controls_query = """
            INSERT INTO user_controls (user_id, is_banned, is_suspicious, force_disconnect, created_at, updated_at)
            VALUES (%s, FALSE, FALSE, FALSE, NOW(), NOW())
        """
        cursor.execute(controls_query, (new_user_id,))
        
        # Asignar rol de STUDENT por defecto
        role_query = """
            INSERT INTO user_roles (user_id, role_id, created_at)
            VALUES (%s, 3, NOW())
        """
        cursor.execute(role_query, (new_user_id,))
        
        conn.commit()
        final_response["data"] = {"user_id": new_user_id}
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while registering user with verification: {e}")
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
            UPDATE users 
            SET email_verified = TRUE, 
                verification_token = NULL, 
                verification_expires_at = NULL,
                updated_at = NOW()
            WHERE id = %s
        """
        cursor.execute(query, (user_id,))
        conn.commit()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while marking user as verified: {e}")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def update_user_verification_token(final_response, conn, cursor, user_id, verification_token, verification_expires_at, request_id):
    try:
        query = """
            UPDATE users 
            SET verification_token = %s, 
                verification_expires_at = %s,
                updated_at = NOW()
            WHERE id = %s
        """
        cursor.execute(query, (verification_token, verification_expires_at, user_id))
        conn.commit()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while updating verification token: {e}")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_user_verification_status(final_response, conn, cursor, username, request_id):
    try:
        query = """
            SELECT email_verified
            FROM users
            WHERE username = %s
            LIMIT 1
        """
        cursor.execute(query, (username,))
        final_response["data"] = cursor.fetchone()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while getting user verification status: {e}")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def update_user_password(final_response, conn, cursor, user_id, new_password, request_id):
    try:
        query = """
            UPDATE users 
            SET password = %s,
                updated_at = NOW()
            WHERE id = %s
        """
        cursor.execute(query, (new_password, user_id))
        conn.commit()
    except Exception as e:
        logger.exception(f"{request_id} - an error occurred while updating user password: {e}")
        final_response["ok"] = False

    return final_response
