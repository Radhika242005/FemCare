from flask import Blueprint, request, jsonify
from backend.database import get_db_connection


recommendations_bp = Blueprint(
    "recommendations",
    __name__
)


def add_unique(items, value):

    if value and value not in items:
        items.append(value)


def get_recommendations():

    connection = None
    cursor = None

    try:

        problem = request.args.get("problem")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if problem:

            cursor.execute(
                """
                SELECT
                    id,
                    problem,
                    practice_type,
                    practice_name,
                    description,
                    video_url
                FROM recommendations
                WHERE problem = %s
                ORDER BY id
                """,
                (problem,)
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    problem,
                    practice_type,
                    practice_name,
                    description,
                    video_url
                FROM recommendations
                ORDER BY id
                """
            )

        recommendations = cursor.fetchall()

        return jsonify({
            "success": True,
            "recommendations": recommendations
        }), 200

    except Exception as error:

        print(
            "Recommendation error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to load recommendations.",
            "error":
                str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


recommendations_bp.route(
    "",
    methods=["GET"]
)(get_recommendations)


def get_latest_health_log(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

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
            ORDER BY log_date DESC, id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    except Exception as error:

        print(
            "Health log error:",
            error
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_health_log_problems(user_id):

    health_log = get_latest_health_log(user_id)

    health_problems = []

    if not health_log:
        return health_problems, None

    sleep_hours = health_log.get(
        "sleep_hours"
    )

    try:

        if (
            sleep_hours is not None
            and float(sleep_hours) < 6
        ):

            add_unique(
                health_problems,
                "Poor Sleep"
            )

    except (TypeError, ValueError):

        pass

    stress_score = health_log.get(
        "stress_score"
    )

    try:

        if (
            stress_score is not None
            and float(stress_score) >= 7
        ):

            add_unique(
                health_problems,
                "High Stress"
            )

    except (TypeError, ValueError):

        pass

    exercise_minutes = health_log.get(
        "exercise_minutes"
    )

    try:

        if (
            exercise_minutes is not None
            and float(exercise_minutes) == 0
        ):

            add_unique(
                health_problems,
                "Physical Activity"
            )

    except (TypeError, ValueError):

        pass

    return health_problems, health_log


def get_user_profile(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                age,
                bmi,
                diet_quality,
                exercise_frequency,
                sleep_hours,
                water_intake_liters,
                caffeine_intake,
                birth_control_use,
                pcos_diagnosed,
                alcohol_consumption,
                smoking_status,
                stress_score,
                stress_score_baseline,
                weight_gain,
                hair_growth,
                skin_darkening,
                hair_loss,
                pimples,
                fast_food
            FROM health_profiles
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    except Exception as error:

        print(
            "Profile error:",
            error
        )

        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_period_analysis(user_id):

    try:

        from services.recommendation_engine import (
            analyze_user_data
        )

        result = analyze_user_data(user_id)

        return result if result else {}

    except Exception as error:

        print(
            "Period analysis error:",
            error
        )

        return {}


def get_pcos_analysis(user_id):

    try:

        from services.pcos_engine import (
            analyze_pcos_user
        )

        result = analyze_pcos_user(user_id)

        return result if result else {}

    except Exception as error:

        print(
            "PCOS analysis error:",
            error
        )

        return {}


def build_pcos_problems(
    profile,
    pcos_analysis
):

    pcos_problems = []

    if not profile:
        profile = {}

    reference_result = (
        pcos_analysis.get(
            "reference_result",
            {}
        )
        if pcos_analysis
        else {}
    )

    positive_percentage = (
        reference_result.get(
            "positive_percentage",
            0
        )
        or 0
    )

    if positive_percentage >= 50:

        add_unique(
            pcos_problems,
            "PCOS Lifestyle Support"
        )

    if str(
        profile.get(
            "weight_gain",
            ""
        )
    ).lower() == "yes":

        add_unique(
            pcos_problems,
            "Weight Management"
        )

    if str(
        profile.get(
            "hair_growth",
            ""
        )
    ).lower() == "yes":

        add_unique(
            pcos_problems,
            "Hormonal Symptom Support"
        )

    if str(
        profile.get(
            "skin_darkening",
            ""
        )
    ).lower() == "yes":

        add_unique(
            pcos_problems,
            "Skin Health"
        )

    if str(
        profile.get(
            "hair_loss",
            ""
        )
    ).lower() == "yes":

        add_unique(
            pcos_problems,
            "Hair Health"
        )

    if str(
        profile.get(
            "pimples",
            ""
        )
    ).lower() == "yes":

        add_unique(
            pcos_problems,
            "Skin Health"
        )

    diet_quality = str(
        profile.get(
            "diet_quality",
            ""
        )
    ).lower()

    if diet_quality == "poor":

        add_unique(
            pcos_problems,
            "PCOS Nutrition"
        )

    exercise = str(
        profile.get(
            "exercise_frequency",
            ""
        )
    ).lower()

    if exercise in [
        "never",
        "rarely"
    ]:

        add_unique(
            pcos_problems,
            "Physical Activity"
        )

    return pcos_problems


def get_recommendations_for_problems(
    problems
):

    if not problems:
        return []

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        placeholders = ",".join(
            ["%s"] * len(problems)
        )

        query = f"""
            SELECT
                id,
                problem,
                practice_type,
                practice_name,
                description,
                video_url
            FROM recommendations
            WHERE problem IN ({placeholders})
        """

        cursor.execute(
            query,
            tuple(problems)
        )

        return cursor.fetchall()

    except Exception as error:

        print(
            "Recommendation database error:",
            error
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def order_recommendations(
    recommendations,
    problems
):

    if not recommendations:
        return []

    priority = {
        problem: index
        for index, problem
        in enumerate(problems)
    }

    recommendations.sort(
        key=lambda item: (
            priority.get(
                item.get("problem"),
                999
            ),
            item.get("id", 999)
        )
    )

    unique = []
    seen_ids = set()

    for recommendation in recommendations:

        recommendation_id = recommendation.get(
            "id"
        )

        if recommendation_id in seen_ids:
            continue

        seen_ids.add(
            recommendation_id
        )

        unique.append(
            recommendation
        )

    return unique


def get_completed_recommendations(
    user_id
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                recommendation_id,
                completed_at
            FROM completed_recommendations
            WHERE user_id = %s
            ORDER BY completed_at DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        return rows

    except Exception as error:

        print(
            "Completed recommendations error:",
            error
        )

        return []

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


def analyze_complete_user(user_id):

    profile = get_user_profile(
        user_id
    )

    period_analysis = get_period_analysis(
        user_id
    )

    pcos_analysis = get_pcos_analysis(
        user_id
    )

    (
        health_log_problems,
        latest_health_log
    ) = get_health_log_problems(
        user_id
    )

    period_problems = list(
        period_analysis.get(
            "problems",
            []
        )
        if period_analysis
        else []
    )

    pcos_problems = build_pcos_problems(
        profile,
        pcos_analysis
    )

    problems = []

    for problem in health_log_problems:

        add_unique(
            problems,
            problem
        )

    for problem in period_problems:

        add_unique(
            problems,
            problem
        )

    for problem in pcos_problems:

        add_unique(
            problems,
            problem
        )

    recommendations = (
        get_recommendations_for_problems(
            problems
        )
    )

    recommendations = order_recommendations(
        recommendations,
        problems
    )

    reference_result = (
        pcos_analysis.get(
            "reference_result",
            {}
        )
        if pcos_analysis
        else {}
    )

    positive_percentage = (
        reference_result.get(
            "positive_percentage",
            0
        )
        or 0
    )

    similar_records = (
        pcos_analysis.get(
            "similar_records_used",
            0
        )
        if pcos_analysis
        else 0
    )

    completed_rows = (
        get_completed_recommendations(
            user_id
        )
    )

    completed_ids = [
        row["recommendation_id"]
        for row in completed_rows
    ]

    return {

        "cycle_number":
            period_analysis.get(
                "cycle_number"
            )
            if period_analysis
            else None,

        "data_source":
            "period_pcos_and_health_log_analysis",

        "health_log_problems":
            health_log_problems,

        "latest_health_log":
            latest_health_log,

        "period_problems":
            period_problems,

        "pcos_problems":
            pcos_problems,

        "problems":
            problems,

        "pcos_reference": {

            "pcos_negative":
                reference_result.get(
                    "pcos_negative",
                    0
                ),

            "pcos_positive":
                reference_result.get(
                    "pcos_positive",
                    0
                ),

            "positive_percentage":
                positive_percentage,

            "similar_records":
                similar_records
        },

        "recommendations":
            recommendations,

        "completed_recommendation_ids":
            completed_ids,

        "medical_notice":
            "PCOS-related information is based on reference dataset patterns and is not a medical diagnosis."
    }


@recommendations_bp.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def get_user_recommendations(user_id):

    try:

        result = analyze_complete_user(
            user_id
        )

        return jsonify({
            "success": True,
            **result
        }), 200

    except Exception as error:

        print(
            "User recommendation error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to generate recommendations.",
            "error":
                str(error)
        }), 500


@recommendations_bp.route(
    "/completed/<int:user_id>",
    methods=["GET"]
)
def get_completed(user_id):

    try:

        rows = get_completed_recommendations(
            user_id
        )

        return jsonify({
            "success": True,
            "completed": rows,
            "completed_recommendation_ids": [
                row["recommendation_id"]
                for row in rows
            ]
        }), 200

    except Exception as error:

        print(
            "Get completed error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to load completed practices.",
            "error":
                str(error)
        }), 500


@recommendations_bp.route(
    "/complete",
    methods=["POST"]
)
def complete_recommendation():

    connection = None
    cursor = None

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "success": False,
                "message":
                    "Request body is required."
            }), 400

        user_id = data.get(
            "user_id"
        )

        recommendation_id = data.get(
            "recommendation_id"
        )

        if not user_id or not recommendation_id:

            return jsonify({
                "success": False,
                "message":
                    "user_id and recommendation_id are required."
            }), 400

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT id
            FROM recommendations
            WHERE id = %s
            LIMIT 1
            """,
            (recommendation_id,)
        )

        recommendation = cursor.fetchone()

        if not recommendation:

            return jsonify({
                "success": False,
                "message":
                    "Recommendation not found."
            }), 404

        cursor.execute(
            """
            SELECT id
            FROM completed_recommendations
            WHERE user_id = %s
              AND recommendation_id = %s
            LIMIT 1
            """,
            (
                user_id,
                recommendation_id
            )
        )

        existing = cursor.fetchone()

        if existing:

            return jsonify({
                "success": True,
                "already_completed": True,
                "message":
                    "Recommendation already completed."
            }), 200

        cursor.execute(
            """
            INSERT INTO completed_recommendations
            (
                user_id,
                recommendation_id
            )
            VALUES (%s, %s)
            """,
            (
                user_id,
                recommendation_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "already_completed": False,
            "message":
                "Recommendation marked as completed.",
            "recommendation_id":
                recommendation_id
        }), 201

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "Complete recommendation error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to mark recommendation as completed.",
            "error":
                str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@recommendations_bp.route(
    "/complete",
    methods=["DELETE"]
)
def remove_completed_recommendation():

    connection = None
    cursor = None

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "success": False,
                "message":
                    "Request body is required."
            }), 400

        user_id = data.get(
            "user_id"
        )

        recommendation_id = data.get(
            "recommendation_id"
        )

        if not user_id or not recommendation_id:

            return jsonify({
                "success": False,
                "message":
                    "user_id and recommendation_id are required."
            }), 400

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM completed_recommendations
            WHERE user_id = %s
              AND recommendation_id = %s
            """,
            (
                user_id,
                recommendation_id
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message":
                "Recommendation marked as incomplete."
        }), 200

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "Remove completion error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to remove completion.",
            "error":
                str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@recommendations_bp.route(
    "/analyze/<int:user_id>",
    methods=["GET"]
)
def analyze_user(user_id):

    try:

        result = analyze_complete_user(
            user_id
        )

        return jsonify({
            "success": True,
            **result
        }), 200

    except Exception as error:

        print(
            "Analysis error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to analyze user data.",
            "error":
                str(error)
        }), 500


@recommendations_bp.route(
    "/streak/<int:user_id>",
    methods=["GET"]
)
def get_wellness_streak(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT DISTINCT
                DATE(completed_at) AS completed_date
            FROM completed_recommendations
            WHERE user_id = %s
            ORDER BY completed_date DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        dates = []

        for row in rows:

            value = row.get(
                "completed_date"
            )

            if value:

                dates.append(
                    value
                )

        if not dates:

            return jsonify({
                "success": True,
                "streak": 0
            }), 200

        from datetime import date, timedelta

        today = date.today()

        latest_date = dates[0]

        if latest_date < (
            today - timedelta(days=1)
        ):

            return jsonify({
                "success": True,
                "streak": 0
            }), 200

        streak = 1

        current_date = latest_date

        for next_date in dates[1:]:

            expected_date = (
                current_date -
                timedelta(days=1)
            )

            if next_date == expected_date:

                streak += 1

                current_date = next_date

            elif next_date < expected_date:

                break

        return jsonify({
            "success": True,
            "streak": streak
        }), 200

    except Exception as error:

        print(
            "Streak error:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to calculate wellness streak.",
            "error":
                str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()