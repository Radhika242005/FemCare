from flask import Blueprint, request, jsonify
from database import get_db_connection

early_puberty_bp = Blueprint(
    "early_puberty",
    __name__
)


@early_puberty_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_early_puberty():

    connection = None
    cursor = None

    try:

        # ========================================================
        # GET DATA
        # ========================================================

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400


        # ========================================================
        # USER ID
        # ========================================================

        user_id = data.get("user_id")

        if not user_id:

            return jsonify({
                "success": False,
                "message": "User ID is required."
            }), 400


        # ========================================================
        # AGE
        # ========================================================

        age = data.get("age")

        if age in (None, ""):

            return jsonify({
                "success": False,
                "message": "Age is required."
            }), 400


        try:

            age = int(age)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Age must be a valid number."
            }), 400


        if age < 1 or age > 18:

            return jsonify({
                "success": False,
                "message": "Age must be between 1 and 18."
            }), 400


        # ========================================================
        # GET PUBERTY SIGNS
        # ========================================================

        puberty_signs = data.get(
            "puberty_signs"
        )

        breast = data.get(
            "early_breast_development"
        )

        pubic_hair = data.get(
            "early_pubic_hair"
        )

        underarm_hair = data.get(
            "early_underarm_hair"
        )

        body_odor = data.get(
            "body_odor"
        )

        acne = data.get(
            "acne"
        )

        rapid_growth = data.get(
            "rapid_growth"
        )

        vaginal_bleeding = data.get(
            "vaginal_bleeding"
        )


        # ========================================================
        # CREATE SYMPTOM DICTIONARY
        # ========================================================

        symptoms = {

            "Puberty signs":
                puberty_signs,

            "Early breast development":
                breast,

            "Early pubic hair":
                pubic_hair,

            "Early underarm hair":
                underarm_hair,

            "Body odor":
                body_odor,

            "Acne":
                acne,

            "Rapid growth":
                rapid_growth,

            "Vaginal bleeding":
                vaginal_bleeding
        }


        # ========================================================
        # FIND SELECTED SIGNS
        # ========================================================

        selected_signs = []


        for sign_name, value in symptoms.items():

            if (
                value is not None
                and str(value).strip().lower() == "yes"
            ):

                selected_signs.append(
                    sign_name
                )


        positive_signs = len(
            selected_signs
        )


        # ========================================================
        # AGE GROUP
        # ========================================================

        if age < 8:

            age_group = (
                "younger than 8 years"
            )

        elif age < 10:

            age_group = (
                "8 to 9 years"
            )

        else:

            age_group = (
                "10 years or older"
            )


        # ========================================================
        # PERSONALIZED RESULT
        # ========================================================

        # --------------------------------------------------------
        # AGE BELOW 8 + MANY SIGNS
        # --------------------------------------------------------

        if age < 8 and positive_signs >= 4:

            result = (
                f"The child is {age} years old and "
                f"{positive_signs} puberty-related signs "
                f"were selected. The selected signs include: "
                f"{', '.join(selected_signs)}. "
                f"Because multiple puberty-related signs "
                f"were reported in this age group, the "
                f"information may warrant further evaluation "
                f"by a qualified healthcare professional."
            )


        # --------------------------------------------------------
        # AGE BELOW 8 + SOME SIGNS
        # --------------------------------------------------------

        elif age < 8 and positive_signs >= 2:

            result = (
                f"The child is {age} years old and "
                f"{positive_signs} puberty-related signs "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"These recorded signs may warrant "
                f"further evaluation, particularly if "
                f"they are progressing."
            )


        # --------------------------------------------------------
        # AGE BELOW 8 + ONE SIGN
        # --------------------------------------------------------

        elif age < 8 and positive_signs == 1:

            result = (
                f"The child is {age} years old and "
                f"one puberty-related sign was selected: "
                f"{selected_signs[0]}. "
                f"Continue monitoring the information "
                f"and consider professional evaluation "
                f"if the sign persists or progresses."
            )


        # --------------------------------------------------------
        # AGE BELOW 8 + NO SIGNS
        # --------------------------------------------------------

        elif age < 8 and positive_signs == 0:

            result = (
                f"The child is {age} years old and "
                f"no puberty-related signs were selected. "
                f"The current information does not show "
                f"strong early-puberty reference indicators."
            )


        # --------------------------------------------------------
        # AGE 8-9 + MANY SIGNS
        # --------------------------------------------------------

        elif age < 10 and positive_signs >= 5:

            result = (
                f"The child is {age} years old and "
                f"multiple puberty-related signs were "
                f"selected: "
                f"{', '.join(selected_signs)}. "
                f"The combination of recorded signs may "
                f"warrant discussion with a qualified "
                f"healthcare professional."
            )


        # --------------------------------------------------------
        # AGE 8-9 + SOME SIGNS
        # --------------------------------------------------------

        elif age < 10 and positive_signs >= 3:

            result = (
                f"The child is {age} years old and "
                f"{positive_signs} puberty-related signs "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"These recorded signs should be monitored, "
                f"especially if they appear or progress "
                f"rapidly."
            )


        # --------------------------------------------------------
        # AGE 8-9 + FEW SIGNS
        # --------------------------------------------------------

        elif age < 10 and positive_signs > 0:

            result = (
                f"The child is {age} years old and "
                f"the following puberty-related sign(s) "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"The current information contains some "
                f"puberty-related indicators."
            )


        # --------------------------------------------------------
        # AGE 8-9 + NO SIGNS
        # --------------------------------------------------------

        elif age < 10 and positive_signs == 0:

            result = (
                f"The child is {age} years old and "
                f"no puberty-related signs were selected. "
                f"The current information does not show "
                f"strong early-puberty reference indicators."
            )


        # --------------------------------------------------------
        # AGE 10+ + MANY SIGNS
        # --------------------------------------------------------

        elif age >= 10 and positive_signs >= 5:

            result = (
                f"The child is {age} years old and "
                f"{positive_signs} puberty-related signs "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"The recorded information shows several "
                f"puberty-related indicators. Continued "
                f"monitoring may be appropriate."
            )


        # --------------------------------------------------------
        # AGE 10+ + SOME SIGNS
        # --------------------------------------------------------

        elif age >= 10 and positive_signs >= 3:

            result = (
                f"The child is {age} years old and "
                f"{positive_signs} puberty-related signs "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"The current information contains several "
                f"puberty-related indicators."
            )


        # --------------------------------------------------------
        # AGE 10+ + FEW SIGNS
        # --------------------------------------------------------

        elif age >= 10 and positive_signs > 0:

            result = (
                f"The child is {age} years old and "
                f"the following puberty-related sign(s) "
                f"were selected: "
                f"{', '.join(selected_signs)}. "
                f"The current information contains some "
                f"puberty-related indicators."
            )


        # --------------------------------------------------------
        # AGE 10+ + NO SIGNS
        # --------------------------------------------------------

        else:

            result = (
                f"The child is {age} years old and "
                f"no puberty-related signs were selected. "
                f"The current information does not show "
                f"strong early-puberty reference indicators."
            )


        # ========================================================
        # DATABASE CONNECTION
        # ========================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ========================================================
        # SAVE ANALYSIS
        # ========================================================

        cursor.execute(
            """
            INSERT INTO early_puberty_logs
            (
                user_id,
                age,
                puberty_signs,
                early_breast_development,
                early_pubic_hair,
                early_underarm_hair,
                body_odor,
                acne,
                rapid_growth,
                vaginal_bleeding,
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
                %s
            )
            """,
            (
                user_id,
                age,
                puberty_signs,
                breast,
                pubic_hair,
                underarm_hair,
                body_odor,
                acne,
                rapid_growth,
                vaginal_bleeding,
                result
            )
        )


        connection.commit()


        # ========================================================
        # RESPONSE
        # ========================================================

        return jsonify({

            "success": True,

            "user_id":
                user_id,

            "age":
                age,

            "positive_signs":
                positive_signs,

            "selected_signs":
                selected_signs,

            "result":
                result,

            "medical_notice":
                "This is a reference screening result based on the information provided and is not a medical diagnosis."

        }), 200


    # ============================================================
    # ERROR HANDLING
    # ============================================================

    except Exception as error:

        if connection:

            connection.rollback()


        print(
            "========================================"
        )

        print(
            "EARLY PUBERTY ANALYSIS ERROR"
        )

        print(
            type(error).__name__
        )

        print(
            str(error)
        )

        print(
            "========================================"
        )


        return jsonify({

            "success":
                False,

            "message":
                "Unable to analyze early puberty data.",

            "error":
                str(error)

        }), 500


    # ============================================================
    # CLOSE DATABASE
    # ============================================================

    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()