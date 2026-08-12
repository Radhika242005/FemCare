from flask import Blueprint, request, jsonify
from database import get_db_connection


food_bp = Blueprint(
    "food",
    __name__
)


@food_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_food():

    connection = None
    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                    "No data received."

            }), 400


        user_id = data.get(
            "user_id"
        )

        if not user_id:

            return jsonify({

                "success": False,

                "message":
                    "User ID is required."

            }), 400


        log_date = data.get(
            "log_date"
        )

        if not log_date:

            return jsonify({

                "success": False,

                "message":
                    "Log date is required."

            }), 400


        try:

            meals_per_day = int(
                data.get(
                    "meals_per_day"
                ) or 0
            )

            fruits = float(
                data.get(
                    "fruits_servings"
                ) or 0
            )

            vegetables = float(
                data.get(
                    "vegetables_servings"
                ) or 0
            )

            protein = float(
                data.get(
                    "protein_servings"
                ) or 0
            )

            water = float(
                data.get(
                    "water_intake_liters"
                ) or 0
            )

        except ValueError:

            return jsonify({

                "success": False,

                "message":
                    "Please enter valid numeric values."

            }), 400


        fast_food = data.get(
            "fast_food"
        )

        sugary_drinks = data.get(
            "sugary_drinks"
        )

        breakfast = data.get(
            "breakfast"
        )

        dietary_preference = data.get(
            "dietary_preference"
        )


        # ====================================================
        # NUTRITION SCORE
        # ====================================================

        score = 0


        # ----------------------------------------------------
        # MEALS
        # ----------------------------------------------------

        if meals_per_day >= 3:

            score += 15

            meals_status = "Good"

        elif meals_per_day >= 2:

            score += 10

            meals_status = "Moderate"

        else:

            meals_status = "Needs Improvement"


        # ----------------------------------------------------
        # FRUITS
        # ----------------------------------------------------

        if fruits >= 2:

            score += 15

            fruits_status = "Good"

        elif fruits >= 1:

            score += 8

            fruits_status = "Moderate"

        else:

            fruits_status = "Needs Improvement"


        # ----------------------------------------------------
        # VEGETABLES
        # ----------------------------------------------------

        if vegetables >= 3:

            score += 20

            vegetables_status = "Good"

        elif vegetables >= 1:

            score += 10

            vegetables_status = "Moderate"

        else:

            vegetables_status = "Needs Improvement"


        # ----------------------------------------------------
        # PROTEIN
        # ----------------------------------------------------

        if protein >= 2:

            score += 15

            protein_status = "Good"

        elif protein >= 1:

            score += 8

            protein_status = "Moderate"

        else:

            protein_status = "Needs Improvement"


        # ----------------------------------------------------
        # WATER
        # ----------------------------------------------------

        if water >= 2:

            score += 15

            water_status = "Good"

        elif water >= 1:

            score += 8

            water_status = "Moderate"

        else:

            water_status = "Needs Improvement"


        # ----------------------------------------------------
        # FAST FOOD
        # ----------------------------------------------------

        if fast_food == "No":

            score += 5

            fast_food_status = "Good"

        else:

            fast_food_status = "Needs Improvement"


        # ----------------------------------------------------
        # SUGARY DRINKS
        # ----------------------------------------------------

        if sugary_drinks == "No":

            score += 5

            sugary_drinks_status = "Good"

        else:

            sugary_drinks_status = "Needs Improvement"


        # ----------------------------------------------------
        # BREAKFAST
        # ----------------------------------------------------

        if breakfast == "Yes":

            score += 5

            breakfast_status = "Good"

        else:

            breakfast_status = "Needs Improvement"


        # ====================================================
        # OVERALL RESULT
        # ====================================================

        if score >= 75:

            nutrition_level = "Good"

            result = (
                "Your selected food pattern shows "
                "strong nutrition reference indicators."
            )

        elif score >= 50:

            nutrition_level = "Moderate"

            result = (
                "Your selected food pattern shows "
                "moderate nutrition reference indicators."
            )

        else:

            nutrition_level = "Needs Improvement"

            result = (
                "Your selected food pattern may benefit "
                "from improved nutrition habits."
            )


        # ====================================================
        # AREAS TO IMPROVE
        # ====================================================

        improvements = []


        if meals_status == "Needs Improvement":

            improvements.append(
                "Regular meals"
            )


        if fruits_status == "Needs Improvement":

            improvements.append(
                "Fruit intake"
            )


        if vegetables_status == "Needs Improvement":

            improvements.append(
                "Vegetable intake"
            )


        if protein_status == "Needs Improvement":

            improvements.append(
                "Protein intake"
            )


        if water_status == "Needs Improvement":

            improvements.append(
                "Water intake"
            )


        if fast_food_status == "Needs Improvement":

            improvements.append(
                "Fast food consumption"
            )


        if sugary_drinks_status == "Needs Improvement":

            improvements.append(
                "Sugary drink consumption"
            )


        if breakfast_status == "Needs Improvement":

            improvements.append(
                "Breakfast habit"
            )


        # ====================================================
        # RECOMMENDATIONS
        # ====================================================

        recommendations = []


        if meals_status != "Good":

            recommendations.append(
                "Try to maintain regular balanced meals "
                "throughout the day."
            )


        if fruits_status != "Good":

            recommendations.append(
                "Include more fruits in your daily diet."
            )


        if vegetables_status != "Good":

            recommendations.append(
                "Add more vegetables to your meals."
            )


        if protein_status != "Good":

            recommendations.append(
                "Include suitable protein sources "
                "in your meals."
            )


        if water_status != "Good":

            recommendations.append(
                "Increase your daily water intake."
            )


        if fast_food_status != "Good":

            recommendations.append(
                "Try to reduce frequent fast-food consumption."
            )


        if sugary_drinks_status != "Good":

            recommendations.append(
                "Consider reducing sugary drinks."
            )


        if breakfast_status != "Good":

            recommendations.append(
                "Consider maintaining a regular breakfast habit."
            )


        if not recommendations:

            recommendations.append(
                "Continue maintaining your current "
                "balanced nutrition habits."
            )


        # ====================================================
        # DATABASE CONNECTION
        # ====================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ====================================================
        # SAVE FOOD LOG
        # ====================================================

        cursor.execute(

            """
            INSERT INTO food_logs
            (
                user_id,
                log_date,
                meals_per_day,
                fruits_servings,
                vegetables_servings,
                protein_servings,
                water_intake_liters,
                fast_food,
                sugary_drinks,
                breakfast,
                dietary_preference,
                nutrition_score,
                reference_result
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
                %s
            )
            """,

            (
                user_id,
                log_date,
                meals_per_day,
                fruits,
                vegetables,
                protein,
                water,
                fast_food,
                sugary_drinks,
                breakfast,
                dietary_preference,
                score,
                result
            )

        )


        connection.commit()


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "user_id":
                user_id,

            "nutrition_score":
                score,

            "nutrition_level":
                nutrition_level,

            "result":
                result,

            "indicators": {

                "meals":
                    meals_status,

                "fruits":
                    fruits_status,

                "vegetables":
                    vegetables_status,

                "protein":
                    protein_status,

                "water":
                    water_status,

                "fast_food":
                    fast_food_status,

                "sugary_drinks":
                    sugary_drinks_status,

                "breakfast":
                    breakfast_status

            },

            "improvements":
                improvements,

            "recommendations":
                recommendations,

            "medical_notice":
                "This is a wellness reference "
                "analysis and is not a medical diagnosis."

        }), 200


    except Exception as error:

        if connection:

            connection.rollback()


        print(
            "Food analysis error:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Unable to analyze food data.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()