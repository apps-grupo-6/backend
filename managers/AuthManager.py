from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
def check_otp_token(final_response, conn, cursor, user_id, otp_token, type, request_id):
    try:
        query = """
            SELECT expires_at
            FROM otp_tokens
            WHERE 
                user_id = %s
                AND token = %s
                AND type = %s
            LIMIT 1;
        """
        values = (user_id, otp_token, type)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking user otp token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def check_if_user_exists(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT jsonb_object_agg(user_id, payload) AS data
            FROM (
                SELECT
                    u.id AS user_id,
                    jsonb_build_object(
                        'banned', uc.is_banned,
                        'suspect', uc.is_suspicious,
                        'forced_disconnect', uc.force_disconnect,
                        'information', jsonb_build_object(
                            'first_name', ui.first_name,
                            'last_name', ui.last_name,
                            'contact_email', ui.contact_email,
                            'telephone', ui.telephone
                        ),
                        'permissions', COALESCE(
                            jsonb_agg(
                                jsonb_build_object(up.method || '-' || up.endpoint, up.id)
                            ) FILTER (WHERE up.id IS NOT NULL),
                            '[]'::jsonb
                        ),
                        'roles', COALESCE(
                            jsonb_agg(DISTINCT r.name)
                            FILTER (WHERE r.name IS NOT NULL),
                            '[]'::jsonb
                        )
                    ) AS payload
                FROM users u
                JOIN user_information ui ON ui.user_id = u.id
                JOIN user_controls uc ON uc.user_id = u.id
                LEFT JOIN user_permissions up ON up.user_id = u.id
                LEFT JOIN user_roles ur ON ur.user_id = u.id
                LEFT JOIN roles r ON r.id = ur.role_id
                GROUP BY
                    u.id,
                    uc.is_banned, uc.is_suspicious, uc.force_disconnect,
                    ui.first_name, ui.last_name, ui.contact_email, ui.telephone
            ) t;
        """
        values = (user_id,)

        logger.info(query%values)
        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if user exists")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def set_new_password(final_response, conn, cursor, new_password, user_id, request_id):
    try:
        query = f"""
            UPDATE users
            SET password_updated_at = NOW(),
                password = %s
            WHERE id = %s
        """
        values = (new_password, user_id)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to update user's password")
        final_response["ok"] = False

    return final_response