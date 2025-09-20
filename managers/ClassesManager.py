from configs.ServerConfig import logger
from utils.DatabaseUtils import with_db_connection

@with_db_connection
def check_if_duplicated(final_response, conn, cursor, professor_id, location_id, discipline_id, scheduled_at, request_id):
    try:
        query = """
            SELECT 1
            FROM classes
            WHERE 
                professor_id = %s
                AND location_id = %s
                AND discipline_id = %s
                AND scheduled_at = %s
            LIMIT 1;
        """
        values = (professor_id, location_id, discipline_id)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if the class is repeated")
        final_response["ok"] = False

    return final_response

@with_db_connection
def create_class(final_response, conn, cursor, professor_id, location_id, discipline_id, scheduled_at, max_participants,
                 qr, request_id):
    try:
        query = """
            INSERT INTO classes (professor_id, location_id, discipline_id, scheduled_at, max_participants, qr, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        values = (professor_id, location_id, discipline_id, scheduled_at, max_participants, qr)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while creating the class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def does_class_exist(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT 1
            FROM classes
            WHERE id = %s
            LIMIT 1;
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if class exists")
        final_response["ok"] = False

    return final_response

@with_db_connection
def finish_class(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            UPDATE classes
            SET 
                ended_at = NOW(),
                updated_at = NOW(),
                status = 'FINISHED'
            WHERE id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to finish this class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def update_class(final_response, conn, cursor, update_columns, update_values, request_id):
    try:
        query = f"""
            UPDATE classes
            SET updated_at = NOW(),
                {update_columns}
            WHERE id = %s
        """
        values = update_values

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to finish this class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def get_class_information(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT 
                c.id as class_id,
                ui.first_name as professor_first_name,
                ui.last_name as professor_last_name,
                c.location_id,
                l.city,
                l.address,
                d.name as discipline_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD"T"HH24:MI:SS.MS') as scheduled_at,
                c.max_participants,
                c.status,
                to_char(c.ended_at, 'YYYY-MM-DD"T"HH24:MI:SS.MS') as ended_at,
                c.qr,
                c.created_at,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'participant_id', cp.id,
                            'user_id', cp.user_id,
                            'added_at', cp.added_at,
                            'status', cp.status,
                            'confirmed_at', cp.confirmed_at,
                            'updated_at', cp.updated_at
                        )
                    ) FILTER (WHERE cp.id IS NOT NULL),  '[]'
                ) AS participants
            FROM classes c
            LEFT JOIN user_information ui ON c.professor_id = ui.user_id
            LEFT JOIN locations l ON c.location_id = l.id  
            LEFT JOIN disciplines d ON c.discipline_id = d.id
            LEFT JOIN class_participants cp on c.id = cp.class_id
            WHERE c.id = %s
            GROUP BY 
                c.id, ui.first_name, ui.last_name,
                c.location_id, l.city, l.address, d.name,
                c.scheduled_at, c.max_participants, c.status,
                c.ended_at, c.qr, c.created_at
            LIMIT 1;
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to obtain class information")
        final_response["ok"] = False

    return final_response

@with_db_connection
def get_all_classes(final_response, conn, cursor, request_id):
    # Created by Luciana
    try:
        query = """
            SELECT 
                c.id as class_id,
                ui.first_name as professor_first_name,
                ui.last_name as professor_last_name,
                c.location_id,
                l.city,
                l.address,
                d.name as discipline_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD"T"HH24:MI:SS.MS') as scheduled_at,
                c.max_participants,
                c.status,
                to_char(c.ended_at, 'YYYY-MM-DD"T"HH24:MI:SS.MS') as ended_at,
                c.qr,
                c.created_at,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'participant_id', cp.id,
                            'user_id', cp.user_id,
                            'added_at', cp.added_at,
                            'status', cp.status,
                            'confirmed_at', cp.confirmed_at,
                            'updated_at', cp.updated_at
                        )
                    ) FILTER (WHERE cp.id IS NOT NULL),  '[]'
                ) AS participants
            FROM classes c
            LEFT JOIN user_information ui ON c.professor_id = ui.user_id
            LEFT JOIN locations l ON c.location_id = l.id  
            LEFT JOIN disciplines d ON c.discipline_id = d.id
            LEFT JOIN class_participants cp on c.id = cp.class_id
            ORDER BY c.scheduled_at DESC;
            GROUP BY 
                c.id, ui.first_name, ui.last_name,
                c.location_id, l.city, l.address, d.name,
                c.scheduled_at, c.max_participants, c.status,
                c.ended_at, c.qr, c.created_at
            LIMIT 1;
        """

        cursor.execute(query)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get all classes")
        final_response["ok"] = False

    return final_response

@with_db_connection
def get_class_participants(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT id, 
                   user_id, 
                   status, 
                   confirmed_at, 
                   added_at, 
                   updated_at
            FROM class_participants cp
            WHERE 
                class_id = %s
                AND status = 'CONFIRMED'
        """
        values = (class_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class participants")
        final_response["ok"] = False

    return final_response

@with_db_connection
def add_class_participant(final_response, conn, cursor, class_id, user_id, request_id):
    try:
        query = """
                INSERT INTO class_participants (class_id, user_id, added_at)
                VALUES (%s, %s, NOW())
                """
        values = (class_id, user_id)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while adding participant to class")
        final_response["ok"] = False

    return final_response

@with_db_connection
def get_user_upcoming_classes(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT
                c.id AS class_id,
                ui.first_name AS professor_first_name,
                ui.last_name AS professor_last_name,
                c.scheduled_at AS class_scheduled_at,
                cp.status AS participant_status,
                cp.confirmed_at AS participant_confirmed_at,
                cp.added_at AS participant_added_at,
                cp.updated_at AS participant_updated_at
            FROM class_participants cp
            JOIN classes c ON c.id = cp.class_id
            JOIN user_information ui ON c.professor_id = ui.user_id
            WHERE
                cp.user_id = %s
                AND c.ended_at IS NULL
                AND c.scheduled_at >= NOW()
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@with_db_connection
def update_participants_status(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            UPDATE class_participants cp
            SET 
                status = CASE
                    WHEN cp.status = 'NOT CONFIRMED' THEN 'EXPIRED'
                    WHEN cp.status = 'CONFIRMED' THEN 'ABSENT'
                    WHEN cp.status = 'CHECKED IN' THEN 'PRESENT'
                    ELSE cp.status
                END,
                updated_at = NOW()
            WHERE cp.class_id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@with_db_connection
def cancel_participant(final_response, conn, cursor, user_id, class_id, request_id):
    try:
        query = """
            UPDATE class_participants
            SET status = 'CANCELLED',
                updated_at = NOW()
            WHERE 
                class_id = %s
                AND user_id = %s
                AND status NOT IN ('EXPIRED', 'ABSENT', 'PRESENT', 'CANCELLED')
            RETURNING id;
        """
        values = (class_id, user_id)

        cursor.execute(query, values)
        if cursor.rowcount > 0:
            final_response["data"] = cursor.fetchone()

        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@with_db_connection
def confirm_participant(final_response, conn, cursor, user_id, class_id, request_id):
    try:
        query = """
            UPDATE class_participants
            SET status = 'CONFIRMED',
                updated_at = NOW()
            WHERE 
                class_id = %s
                AND user_id = %s
                AND status NOT IN ('EXPIRED', 'ABSENT', 'PRESENT', 'CANCELLED', 'CONFIRMED')
            RETURNING id;
        """
        values = (class_id, user_id)

        cursor.execute(query, values)
        if cursor.rowcount > 0:
            final_response["data"] = cursor.fetchone()

        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response