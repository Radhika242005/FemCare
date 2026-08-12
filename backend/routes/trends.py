from flask import Blueprint, jsonify
from backend.database import get_db_connection

trends_bp = Blueprint(
    "trends",
    __name__
)


def calculate_trend(values, higher_is_better=True):

    if len(values) < 2:
        return {
            "status": "Not enough data",
            "message": "At least two health logs are required."
        }

    first = values[0]
    last = values[-1]

    difference = last - first

    if difference == 0:
        return {
            "status": "Stable",
            "message": "Your recorded values are relatively stable."
        }

    if higher_is_better:

        if difference > 0:
            return {
                "status": "Improving",
                "message": "Your recorded values have increased."
            }

        return {
            "status": "Decreasing",
            "message": "Your recorded values have decreased."
        }

    else:

        if difference < 0:
            return {
                "status": "Improving",
                "message": "Your recorded score has decreased."
            }

        return {
            "status": "Increasing",
            "message": "Your recorded score has increased."
        }


@trends_bp.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def get_health_trends(user_id):

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
                log_date,
                sleep_hours,
                water_intake_liters,
                stress_score,
                exercise_minutes

            FROM health_logs

            WHERE user_id = %s

            ORDER BY log_date ASC, id ASC
            """,
            (user_id,)
        )

        logs = cursor.fetchall()

        if not logs:

            return jsonify({
                "success": True,
                "user_id": user_id,
                "count": 0,
                "message": "No health log data available.",
                "trends": {},
                "logs": []
            }), 200


        sleep_values = []

        water_values = []

        stress_values = []

        exercise_values = []


        for log in logs:

            if log["sleep_hours"] is not None:

                sleep_values.append(
                    float(log["sleep_hours"])
                )


            if log["water_intake_liters"] is not None:

                water_values.append(
                    float(
                        log["water_intake_liters"]
                    )
                )


            if log["stress_score"] is not None:

                stress_values.append(
                    float(
                        log["stress_score"]
                    )
                )


            if log["exercise_minutes"] is not None:

                exercise_values.append(
                    float(
                        log["exercise_minutes"]
                    )
                )


        trends = {

            "sleep": calculate_trend(
                sleep_values,
                True
            ),

            "water": calculate_trend(
                water_values,
                True
            ),

            "stress": calculate_trend(
                stress_values,
                False
            ),

            "exercise": calculate_trend(
                exercise_values,
                True
            )

        }


        return jsonify({

            "success": True,

            "user_id":
                user_id,

            "count":
                len(logs),

            "data_source":
                "health_logs",

            "trends":
                trends,

            "logs":
                logs

        }), 200


    except Exception as error:

        print(
            "Health trends error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to load health trends.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()