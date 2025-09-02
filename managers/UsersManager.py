from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
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