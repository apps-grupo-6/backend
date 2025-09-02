import psycopg2
import psycopg2.extras
from functools import wraps
from configs.ServerConfig import connection_pool, logger


def with_db_connection(func):
    """
        Manages database connection, executes and return results
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        cursor = None

        final_response = {
            "data": {},
            "ok": True
        }

        try:
            if connection_pool:
                conn = connection_pool.getconn()
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                # Asegurar que siempre se use el esquema public
                cursor.execute("SET search_path TO public;")

                # Ejecuta la función decorada
                result = func(*args, conn=conn, cursor=cursor, final_response=final_response, **kwargs)
                #final_response["data"] = dict(result) if result else None
            else:
                logger.critical("Pool connections is not started")

        except psycopg2.Error as err:
            logger.critical(f"Database error with '{func.__name__}': {err}")

        except Exception as e:
            logger.critical(f"Unexpected error with {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                connection_pool.putconn(conn)

        return final_response

    return wrapper
