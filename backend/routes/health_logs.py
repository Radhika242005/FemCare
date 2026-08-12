from flask import Blueprint, request, jsonify
from backend.database import get_db_connection


health_logs_bp = Blueprint(
    "health_logs",
    __name__
)


# ============================================================
# ADD / UPDATE HEALTH LOG
# ============================================================

@health_logs_bp.route(
    "",
    methods=["POST"]
)
def add_health_log():

    connection = None
    cursor = None

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400


        user_id = data.get("user_id")
        log_date = data.get("log_date")

        sleep_hours = data.get(
            "sleep_hours"
        )

        water_intake_liters = data.get(
            "water_intake_liters"
        )

        stress_score = data.get(
            "stress_score"
        )

        exercise_minutes = data.get(
            "exercise_minutes"
        )


        # ====================================================
        # VALIDATION
        # ====================================================

        if not user_id:

            return jsonify({
                "success": False,
                "message": "User ID is required."
            }), 400


        if not log_date:

            return jsonify({
                "success": False,
                "message": "Log date is required."
            }), 400


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ====================================================
        # CHECK EXISTING LOG
        # ====================================================

        cursor.execute(
            """
            SELECT id
            FROM health_logs

            WHERE user_id = %s
            AND log_date = %s
            """,
            (
                user_id,
                log_date
            )
        )

        existing = cursor.fetchone()


        # ====================================================
        # UPDATE EXISTING LOG
        # ====================================================

        if existing:

            cursor.execute(
                """
                UPDATE health_logs

                SET
                    sleep_hours = %s,
                    water_intake_liters = %s,
                    stress_score = %s,
                    exercise_minutes = %s

                WHERE user_id = %s
                AND log_date = %s
                """,
                (
                    sleep_hours,
                    water_intake_liters,
                    stress_score,
                    exercise_minutes,
                    user_id,
                    log_date
                )
            )

            connection.commit()


            return jsonify({

                "success": True,

                "message":
                    "Health log updated successfully.",

                "log_id":
                    existing["id"]

            }), 200


        # ====================================================
        # INSERT NEW LOG
        # ====================================================

        cursor.execute(
            """
            INSERT INTO health_logs
            (
                user_id,
                log_date,
                sleep_hours,
                water_intake_liters,
                stress_score,
                exercise_minutes
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                log_date,
                sleep_hours,
                water_intake_liters,
                stress_score,
                exercise_minutes
            )
        )


        connection.commit()


        return jsonify({

            "success": True,

            "message":
                "Health log saved successfully.",

            "log_id":
                cursor.lastrowid

        }), 201


    except Exception as error:

        if connection:
            connection.rollback()


        print(
            "Health log error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to save health log.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET HEALTH LOGS FOR USER
# ============================================================

@health_logs_bp.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def get_health_logs(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                id,
                user_id,
                log_date,
                sleep_hours,
                water_intake_liters,
                stress_score,
                exercise_minutes,
                created_at

            FROM health_logs

            WHERE user_id = %s

            ORDER BY
                log_date ASC,
                id ASC
            """,
            (user_id,)
        )


        logs = cursor.fetchall()


        return jsonify({

            "success": True,

            "user_id":
                user_id,

            "count":
                len(logs),

            "logs":
                logs

        }), 200


    except Exception as error:

        print(
            "Get health logs error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to load health logs.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()