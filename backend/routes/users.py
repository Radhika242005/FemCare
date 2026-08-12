from flask import Blueprint, request, jsonify

from database import get_db_connection


users_bp = Blueprint(
    "users",
    __name__
)


# ============================================================
# CONVERT EMPTY NUMERIC VALUES TO NULL
# ============================================================

def nullable_number(value):

    if value is None or value == "":
        return None

    return value


# ============================================================
# SAVE / UPDATE HEALTH PROFILE
# ============================================================

@users_bp.route(
    "/profile",
    methods=["POST"]
)
def save_profile():

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

        if not user_id:

            return jsonify({
                "success": False,
                "message": "User ID is required."
            }), 400


        connection = get_db_connection()

        cursor = connection.cursor()


        # ====================================================
        # CHECK EXISTING PROFILE
        # ====================================================

        cursor.execute(
            """
            SELECT id
            FROM health_profiles
            WHERE user_id = %s
            """,
            (user_id,)
        )

        existing_profile = cursor.fetchone()


        # ====================================================
        # UPDATE EXISTING PROFILE
        # ====================================================

        if existing_profile:

            cursor.execute(
                """
                UPDATE health_profiles
                SET
                    age = %s,
                    bmi = %s,
                    diet_quality = %s,
                    exercise_frequency = %s,
                    sleep_hours = %s,
                    caffeine_intake = %s,
                    water_intake_liters = %s,
                    alcohol_consumption = %s,
                    smoking_status = %s,
                    birth_control_use = %s,
                    pcos_diagnosed = %s,
                    stress_score_baseline = %s,
                    weight_gain = %s,
                    hair_growth = %s,
                    skin_darkening = %s,
                    hair_loss = %s,
                    pimples = %s,
                    fast_food = %s
                WHERE user_id = %s
                """,
                (
                    nullable_number(
                        data.get("age")
                    ),

                    nullable_number(
                        data.get("bmi")
                    ),

                    data.get(
                        "diet_quality"
                    ),

                    data.get(
                        "exercise_frequency"
                    ),

                    nullable_number(
                        data.get("sleep_hours")
                    ),

                    data.get(
                        "caffeine_intake"
                    ),

                    nullable_number(
                        data.get(
                            "water_intake_liters"
                        )
                    ),

                    data.get(
                        "alcohol_consumption"
                    ),

                    data.get(
                        "smoking_status"
                    ),

                    data.get(
                        "birth_control_use"
                    ),

                    data.get(
                        "pcos_diagnosed"
                    ),

                    nullable_number(
                        data.get(
                            "stress_score_baseline"
                        )
                    ),

                    data.get(
                        "weight_gain"
                    ),

                    data.get(
                        "hair_growth"
                    ),

                    data.get(
                        "skin_darkening"
                    ),

                    data.get(
                        "hair_loss"
                    ),

                    data.get(
                        "pimples"
                    ),

                    data.get(
                        "fast_food"
                    ),

                    user_id
                )
            )

            message = (
                "Health profile updated successfully."
            )


        # ====================================================
        # CREATE NEW PROFILE
        # ====================================================

        else:

            cursor.execute(
                """
                INSERT INTO health_profiles
                (
                    user_id,
                    age,
                    bmi,
                    diet_quality,
                    exercise_frequency,
                    sleep_hours,
                    caffeine_intake,
                    water_intake_liters,
                    alcohol_consumption,
                    smoking_status,
                    birth_control_use,
                    pcos_diagnosed,
                    stress_score_baseline,
                    weight_gain,
                    hair_growth,
                    skin_darkening,
                    hair_loss,
                    pimples,
                    fast_food
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
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

                    nullable_number(
                        data.get("age")
                    ),

                    nullable_number(
                        data.get("bmi")
                    ),

                    data.get(
                        "diet_quality"
                    ),

                    data.get(
                        "exercise_frequency"
                    ),

                    nullable_number(
                        data.get("sleep_hours")
                    ),

                    data.get(
                        "caffeine_intake"
                    ),

                    nullable_number(
                        data.get(
                            "water_intake_liters"
                        )
                    ),

                    data.get(
                        "alcohol_consumption"
                    ),

                    data.get(
                        "smoking_status"
                    ),

                    data.get(
                        "birth_control_use"
                    ),

                    data.get(
                        "pcos_diagnosed"
                    ),

                    nullable_number(
                        data.get(
                            "stress_score_baseline"
                        )
                    ),

                    data.get(
                        "weight_gain"
                    ),

                    data.get(
                        "hair_growth"
                    ),

                    data.get(
                        "skin_darkening"
                    ),

                    data.get(
                        "hair_loss"
                    ),

                    data.get(
                        "pimples"
                    ),

                    data.get(
                        "fast_food"
                    )
                )
            )

            message = (
                "Health profile saved successfully."
            )


        # ====================================================
        # COMMIT
        # ====================================================

        connection.commit()


        return jsonify({

            "success": True,

            "message": message

        }), 200


    except Exception as error:

        if connection:
            connection.rollback()


        print(
            "Profile error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Server error while saving profile.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET HEALTH PROFILE
# ============================================================

@users_bp.route(
    "/profile/<int:user_id>",
    methods=["GET"]
)
def get_profile(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ====================================================
        # GET USER PROFILE
        # ====================================================

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                age,
                bmi,
                diet_quality,
                exercise_frequency,
                sleep_hours,
                caffeine_intake,
                water_intake_liters,
                alcohol_consumption,
                smoking_status,
                birth_control_use,
                pcos_diagnosed,
                stress_score_baseline,
                weight_gain,
                hair_growth,
                skin_darkening,
                hair_loss,
                pimples,
                fast_food
            FROM health_profiles
            WHERE user_id = %s
            LIMIT 1
            """,
            (user_id,)
        )


        profile = cursor.fetchone()


        # ====================================================
        # PROFILE NOT FOUND
        # ====================================================

        if not profile:

            return jsonify({

                "success": True,

                "profile_exists": False,

                "profile": None,

                "message":
                    "No health profile found."

            }), 200


        # ====================================================
        # PROFILE FOUND
        # ====================================================

        return jsonify({

            "success": True,

            "profile_exists": True,

            "profile": profile

        }), 200


    except Exception as error:

        print(
            "Get profile error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to load health profile.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()