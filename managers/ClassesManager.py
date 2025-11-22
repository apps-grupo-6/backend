from configs.ServerConfig import logger
from utils import DatabaseUtils

from configs import ClassesConfig

@DatabaseUtils.with_db_connection
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
                AND status NOT IN ('CANCELLED', 'FINISHED')
            LIMIT 1;
        """
        values = (professor_id, location_id, discipline_id, scheduled_at)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while checking if the class is repeated")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
def update_class(final_response, conn, cursor, update_columns, update_values, request_id):
    try:
        query = f"""
            UPDATE classes
            SET updated_at = NOW(),
                {update_columns}
            WHERE id = %s
        """
        values = tuple(update_values)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to finish this class")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_class_information(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT 
                c.professor_id as professor_id,
                ui.first_name as professor_first_name,
                ui.last_name as professor_last_name,
                c.location_id as gym_id,
                l.city as gym_city,
                l.name as gym_name,
                l.address as gym_address,
                d.name as class_discipline_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD HH24:MI:SS') as class_scheduled_at,
                c.max_participants as class_max_participants,
                c.status as class_status,
                to_char(c.ended_at, 'YYYY-MM-DD HH24:MI:SS') as class_ended_at,
                c.qr as class_qr,
                to_char(c.created_at, 'YYYY-MM-DD HH24:MI:SS') as class_created_at,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'participant_id', cp.id,
                            'participant_user_id', cp.user_id,
                            'participant_added_at', cp.added_at,
                            'participant_status', cp.status,
                            'participant_confirmed_at', cp.confirmed_at,
                            'participant_updated_at', cp.updated_at
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
                c.location_id, l.city, l.address, l.name, d.name,
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


@DatabaseUtils.with_db_connection
def get_all_classes(final_response, conn, cursor, request_id):
    # Created by Luciana
    try:
        query = """
            SELECT 
                c.id as class_id,
                c.professor_id as professor_id,
                ui.first_name as professor_first_name,
                ui.last_name as professor_last_name,
                c.location_id as gym_id,
                l.city as gym_city,
                l.name as gym_name,
                l.address as gym_address,
                d.name as class_discipline_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD HH24:MI:SS') as class_scheduled_at,
                c.max_participants as class_max_participants,
                c.status as class_status,
                to_char(c.ended_at, 'YYYY-MM-DD HH24:MI:SS') as class_ended_at,
                c.qr as class_qr,
                to_char(c.created_at, 'YYYY-MM-DD HH24:MI:SS') as class_created_at,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'participant_id', cp.id,
                            'participant_user_id', cp.user_id,
                            'participant_added_at', cp.added_at,
                            'participant_status', cp.status,
                            'participant_confirmed_at', cp.confirmed_at,
                            'participant_updated_at', cp.updated_at
                        )
                    ) FILTER (WHERE cp.id IS NOT NULL),  '[]'
                ) AS participants
            FROM classes c
            LEFT JOIN user_information ui ON c.professor_id = ui.user_id
            LEFT JOIN locations l ON c.location_id = l.id  
            LEFT JOIN disciplines d ON c.discipline_id = d.id
            LEFT JOIN class_participants cp on c.id = cp.class_id
            WHERE 
                c.scheduled_at >= NOW()
                AND c.status != 'CANCELLED'
            GROUP BY 
                c.id, ui.first_name, ui.last_name,
                c.location_id, l.city, l.address, l.name, d.name,
                c.scheduled_at, c.max_participants, c.status,
                c.ended_at, c.qr, c.created_at
            ORDER BY c.scheduled_at DESC
        """

        cursor.execute(query)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get all classes")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_class_participants(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            SELECT id as participant_id, 
                   user_id as participant_user_id, 
                   status as participant_status, 
                   confirmed_at as participant_confirmed_at, 
                   added_at as participant_added_at, 
                   updated_at as participant_updated_at
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

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
def get_user_upcoming_classes(final_response, conn, cursor, user_id, request_id):
    try:
        query = """
            SELECT
                c.id AS class_id,
                ui.first_name AS professor_first_name,
                ui.last_name AS professor_last_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD HH24:MI:SS') as class_scheduled_at,
                cp.status AS participant_status,
                to_char(cp.confirmed_at, 'YYYY-MM-DD HH24:MI:SS') as participant_confirmed_at,
                to_char(cp.added_at, 'YYYY-MM-DD HH24:MI:SS') as participant_added_at,
                to_char(cp.updated_at, 'YYYY-MM-DD HH24:MI:SS') as participant_updated_at
            FROM class_participants cp
            JOIN classes c ON c.id = cp.class_id
            JOIN user_information ui ON c.professor_id = ui.user_id
            WHERE
                cp.user_id = %s
                AND c.ended_at IS NULL
                AND c.scheduled_at >= NOW()
                AND c.status = 'NOT STARTED'
        """
        values = (user_id,)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
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

@DatabaseUtils.with_db_connection
def cancel_participant(final_response, conn, cursor, user_id, class_id, request_id):
    try:
        query = """
            UPDATE class_participants
            SET status = 'CANCELLED',
                updated_at = NOW()
            WHERE 
                class_id = %s
                AND user_id = %s
                AND status NOT IN %s
            RETURNING id;
        """
        values = (class_id, user_id, ClassesConfig.BLOCKED_STATUS)

        cursor.execute(query, values)
        if cursor.rowcount > 0:
            final_response["data"] = cursor.fetchone()

        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def confirm_participant(final_response, conn, cursor, user_id, class_id, request_id):
    try:
        query = """
            UPDATE class_participants
            SET status = 'CONFIRMED',
                updated_at = NOW()
            WHERE 
                class_id = %s
                AND user_id = %s
                AND status NOT IN %s
            RETURNING id;
        """
        values = (class_id, user_id, ClassesConfig.BLOCK_CONFIRM_STATUS)

        cursor.execute(query, values)
        if cursor.rowcount > 0:
            final_response["data"] = cursor.fetchone()

        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get class upcoming classes")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def does_participant_exist(final_response, conn, cursor, class_id, user_id, request_id):
    try:
        query = """
            SELECT status as participant_status
            FROM class_participants
            WHERE 
                class_id = %s
                AND user_id = %s
            LIMIT 1;
        """
        values = (class_id, user_id)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchone()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to check if user_id participates in this class")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def get_user_classes_history(final_response, conn, cursor, user_id, columns, column_values, request_id):
    try:
        query = """
            SELECT
                c.id AS class_id,
                ui.first_name AS professor_first_name,
                ui.last_name AS professor_last_name,
                to_char(c.scheduled_at, 'YYYY-MM-DD HH24:MI:SS') as class_scheduled_at,
                cp.status AS participant_status,
                to_char(cp.confirmed_at, 'YYYY-MM-DD HH24:MI:SS') as participant_confirmed_at,
                to_char(cp.added_at, 'YYYY-MM-DD HH24:MI:SS') as participant_added_at,
                to_char(cp.updated_at, 'YYYY-MM-DD HH24:MI:SS') as participant_updated_at,
                l.city AS gym_city,
                l.address AS gym_address,
                l.name AS gym_name,
                CASE
                    WHEN c.ended_at IS NOT NULL THEN (c.ended_at - c.scheduled_at)::TEXT
                    ELSE NULL
                END AS duration
            FROM class_participants cp
            JOIN classes c ON c.id = cp.class_id
            JOIN user_information ui ON c.professor_id = ui.user_id
            JOIN locations l ON c.location_id = l.id
            WHERE
                cp.user_id = %s
                AND (c.scheduled_at < NOW() OR c.status IN ('CANCELLED', 'FINISHED'))
        """

        values = (user_id,)

        if columns:
            query += f"AND {columns}"
            values += tuple(column_values)

        cursor.execute(query, values)
        final_response["data"] = cursor.fetchall()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to get user_id all classes history")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def start_class(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            UPDATE classes
            SET 
                started_at = NOW(),
                updated_at = NOW(),
                status = 'STARTED'
            WHERE id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to start this class")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def cancel_class(final_response, conn, cursor, class_id, request_id):
    try:
        query = """
            UPDATE classes
            SET 
                updated_at = NOW(),
                status = 'CANCELLED'
            WHERE id = %s
        """
        values = (class_id,)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to cancel this class")
        final_response["ok"] = False

    return final_response

@DatabaseUtils.with_db_connection
def check_in_participant(final_response, conn, cursor, class_id, user_id, request_id):
    try:
        query = """
            UPDATE class_participants 
            SET 
                updated_at = NOW(),
                status = 'CHECKED IN'
            WHERE 
                class_id = %s
                AND user_id = %s
        """
        values = (class_id, user_id)

        cursor.execute(query, values)
        conn.commit()
    except:
        logger.exception(f"{request_id} - an error occurred while trying to cancel this class")
        final_response["ok"] = False

    return final_response