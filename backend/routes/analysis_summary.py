from flask import Blueprint, jsonify
from database import get_db_connection

analysis_summary_bp = Blueprint(
    "analysis_summary",
    __name__
)


@analysis_summary_bp.route(
    "/<int:user_id>",
    methods=["GET"]
)
def get_analysis_summary(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        results = {}

        tables = {
            "pcos": "pcos_logs",
            "thyroid": "thyroid_logs",
            "early_puberty": "early_puberty_logs",
            "perimenopause": "perimenopause_logs",
            "menopause": "menopause_logs",
            "postmenopause": "postmenopause_logs",
            "pregnancy": "pregnancy_logs",
            "food": "food_logs"
        }

        for name, table in tables.items():

            try:

                cursor.execute(
                    f"""
                    SELECT *
                    FROM {table}
                    WHERE user_id = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (user_id,)
                )

                results[name] = cursor.fetchone()

            except Exception as error:

                print(
                    f"{table} error:",
                    error
                )

                results[name] = None

        return jsonify({

            "success": True,

            "user_id": user_id,

            "analyses": results

        }), 200

    except Exception as error:

        print(
            "Analysis summary error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to load analysis summary.",

            "error":
                str(error)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()