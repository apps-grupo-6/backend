from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
def create_request_log(final_response, conn, cursor, user_id, method, endpoint, code, execution_time, request_id):
    try:
        query = """
            INSERT INTO requests (id, user_id, method, endpoint, code, execution_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        values = (request_id, user_id, method, endpoint, code, execution_time)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the log")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_users(final_response, conn, cursor):
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
                            'telephone', ui.telephone,
                            'username', u.username
                        ),
                        'permissions', COALESCE(
                            jsonb_object_agg(rp.method || '-' || rp.endpoint, rp.id
                            ) FILTER (WHERE rp.id IS NOT NULL),
                            '{}'::jsonb
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
                LEFT JOIN user_roles ur ON ur.user_id = u.id
                LEFT JOIN roles r ON r.id = ur.role_id
                LEFT JOIN role_permissions rp ON rp.role_id = r.id
                GROUP BY
                    u.id,
                    uc.is_banned, uc.is_suspicious, uc.force_disconnect,
                    ui.first_name, ui.last_name, ui.contact_email, ui.telephone
            ) t;
        """
        cursor.execute(query)
        final_response["data"] = cursor.fetchall()[0]
    except:
        logger.exception(f"an error occurred while retrieving all users")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def set_user_as_suspect(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            UPDATE user_controls
            SET 
                is_suspicious = TRUE,
                suspicious_request_id = %s
            WHERE user_id = %s
        """
        values = (request_id, user_id)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while setting user as suspect")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def set_user_as_banned(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            UPDATE user_controls
            SET 
                is_banned = TRUE,
                ban_request_id = %s
            WHERE user_id = %s
        """
        values = (request_id, user_id)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while banning this user")
        final_response["ok"] = False

    return final_response
