from flask import Blueprint, request, jsonify
from database import get_db_connection

pregnancy_bp = Blueprint(
    "pregnancy",
    __name__
)


@pregnancy_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_pregnancy():

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

        age = data.get("age")

        if age in (None, ""):
            return jsonify({
                "success": False,
                "message": "Age is required."
            }), 400

        age = int(age)

        pregnancy_status = data.get(
            "pregnancy_status"
        )

        gestational_weeks = data.get(
            "gestational_weeks"
        )

        prenatal_visits = data.get(
            "prenatal_visits"
        )

        blood_pressure = data.get(
            "blood_pressure"
        )

        blood_sugar = data.get(
            "blood_sugar"
        )

        nausea = data.get("nausea")
        vomiting = data.get("vomiting")
        fatigue = data.get("fatigue")
        swelling = data.get("swelling")
        headache = data.get("headache")
        abdominal_pain = data.get(
            "abdominal_pain"
        )
        bleeding = data.get("bleeding")


        # =====================================================
        # NUMERIC VALUES
        # =====================================================

        if gestational_weeks in (None, ""):

            gestational_weeks = 0

        else:

            gestational_weeks = float(
                gestational_weeks
            )


        if prenatal_visits in (None, ""):

            prenatal_visits = 0

        else:

            prenatal_visits = int(
                prenatal_visits
            )


        # =====================================================
        # COUNT SYMPTOMS
        # =====================================================

        symptoms = [
            nausea,
            vomiting,
            fatigue,
            swelling,
            headache,
            abdominal_pain,
            bleeding
        ]

        symptom_count = sum(
            1
            for symptom in symptoms
            if str(symptom).lower() == "yes"
        )


        # =====================================================
        # PERSONALIZED RESULT
        # =====================================================

        if pregnancy_status != "Yes":

            result = (
                "The selected information indicates "
                "that the user is not currently pregnant."
            )


        elif (
            abdominal_pain == "Yes"
            and bleeding == "Yes"
        ):

            result = (
                "Both abdominal pain and bleeding were "
                "reported during pregnancy. These selected "
                "indicators may require prompt medical "
                "evaluation."
            )


        elif bleeding == "Yes":

            result = (
                "Bleeding was reported during pregnancy. "
                "This is an important reference indicator "
                "that may require medical evaluation."
            )


        elif abdominal_pain == "Yes":

            result = (
                "Abdominal pain was reported during "
                "pregnancy and may require further "
                "medical evaluation."
            )


        elif (
            blood_pressure == "High"
            and blood_sugar == "High"
        ):

            result = (
                "Both high blood pressure and high blood "
                "sugar were selected. The reference profile "
                "contains multiple health indicators that "
                "may require further medical evaluation."
            )


        elif blood_pressure == "High":

            result = (
                "High blood pressure was selected during "
                "pregnancy. This is a pregnancy-related "
                "reference indicator that may require "
                "further medical evaluation."
            )


        elif blood_sugar == "High":

            result = (
                "High blood sugar was selected during "
                "pregnancy. This is a health-related "
                "reference indicator that may require "
                "further evaluation."
            )


        elif symptom_count >= 5:

            result = (
                "Several pregnancy-related symptoms were "
                "selected. The reference profile contains "
                "multiple symptom indicators."
            )


        elif symptom_count >= 3:

            result = (
                "Several pregnancy-related symptoms were "
                "selected for this reference profile."
            )


        elif prenatal_visits == 0:

            result = (
                "Pregnancy was selected, but no prenatal "
                "visits were recorded in the provided "
                "information."
            )


        elif gestational_weeks > 42:

            result = (
                "The selected gestational period is above "
                "42 weeks. The provided information may "
                "require further medical evaluation."
            )


        elif (
            gestational_weeks > 0
            and prenatal_visits >= 1
        ):

            result = (
                "The selected information shows a current "
                "pregnancy with recorded gestational weeks "
                "and prenatal visits, without strong "
                "additional reference indicators."
            )


        else:

            result = (
                "The selected information does not show "
                "strong pregnancy-related reference "
                "indicators."
            )


        # =====================================================
        # DATABASE
        # =====================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            INSERT INTO pregnancy_logs
            (
                user_id,
                age,
                pregnancy_status,
                gestational_weeks,
                prenatal_visits,
                blood_pressure,
                blood_sugar,
                nausea,
                vomiting,
                fatigue,
                swelling,
                headache,
                abdominal_pain,
                bleeding,
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
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                age,
                pregnancy_status,
                gestational_weeks,
                prenatal_visits,
                blood_pressure,
                blood_sugar,
                nausea,
                vomiting,
                fatigue,
                swelling,
                headache,
                abdominal_pain,
                bleeding,
                result
            )
        )


        connection.commit()


        return jsonify({

            "success": True,

            "user_id": user_id,

            "result": result,

            "medical_notice":
                "This is a reference screening "
                "result based on the information "
                "provided. It is not a medical diagnosis."

        }), 200


    except Exception as error:

        if connection:

            connection.rollback()


        import traceback

        print(
            "\n========================================"
        )

        print(
            "PREGNANCY ANALYSIS ERROR"
        )

        print(
            error
        )

        traceback.print_exc()

        print(
            "========================================\n"
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to analyze pregnancy data.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()