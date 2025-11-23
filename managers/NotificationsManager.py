from configs.ServerConfig import logger
from utils import DatabaseUtils

@DatabaseUtils.with_db_connection
def set_user_token(final_response, conn, cursor, user_id, expo_push_token, request_id):
    try:
        query = """
            INSERT INTO user_push_tokens (user_id, expo_push_token)
            VALUES(%s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET
                expo_push_token = EXCLUDED.expo_push_token,
                updated_at = NOW();
        """
        values = (user_id, expo_push_token)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while setting user expo token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_class_participants_token(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT upt.expo_push_token
            FROM class_participants cp
            JOIN user_push_tokens upt ON cp.user_id = upt.user_id
            WHERE cp.class_id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while setting user expo token")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_user_token(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT upt.expo_push_token
            FROM user_push_tokens upt
            WHERE upt.user_id = %s
            LIMIT 1;
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while setting user expo token")
        final_response["ok"] = False

    return final_response