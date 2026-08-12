from flask import Blueprint, request, jsonify
from backend.database import get_db_connection


thyroid_bp = Blueprint(
    "thyroid",
    __name__
)


@thyroid_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_thyroid():

    connection = None
    cursor = None

    try:

        # ========================================================
        # GET REQUEST DATA
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
        # GET INPUT VALUES
        # ========================================================

        tsh = data.get("tsh")
        t3 = data.get("t3")
        t4 = data.get("t4")

        fatigue = data.get("fatigue")
        weight_change = data.get("weight_change")
        cold_sensitivity = data.get("cold_sensitivity")
        heat_sensitivity = data.get("heat_sensitivity")
        hair_changes = data.get("hair_changes")
        mood_changes = data.get("mood_changes")
        sleep_problems = data.get("sleep_problems")


        # ========================================================
        # CONNECT DATABASE
        # ========================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ========================================================
        # PROCESS SYMPTOMS
        # ========================================================

        symptoms = {

            "Fatigue":
                fatigue,

            "Weight Change":
                weight_change,

            "Cold Sensitivity":
                cold_sensitivity,

            "Heat Sensitivity":
                heat_sensitivity,

            "Hair Changes":
                hair_changes,

            "Mood Changes":
                mood_changes,

            "Sleep Problems":
                sleep_problems
        }


        selected_symptoms = []


        for symptom_name, value in symptoms.items():

            if (
                value is not None
                and str(value).strip().lower() == "yes"
            ):

                selected_symptoms.append(
                    symptom_name
                )


        symptom_count = len(
            selected_symptoms
        )


        # ========================================================
        # PROCESS LAB VALUES
        # ========================================================

        abnormal_values = 0

        abnormal_tests = []


        try:

            # -----------------------------
            # TSH
            # -----------------------------

            if tsh not in (None, ""):

                tsh_value = float(tsh)

                if tsh_value > 4.5:

                    abnormal_values += 1

                    abnormal_tests.append(
                        "TSH"
                    )


            # -----------------------------
            # T3
            # -----------------------------

            if t3 not in (None, ""):

                t3_value = float(t3)

                if t3_value < 0.8:

                    abnormal_values += 1

                    abnormal_tests.append(
                        "T3"
                    )


            # -----------------------------
            # T4
            # -----------------------------

            if t4 not in (None, ""):

                t4_value = float(t4)

                if t4_value < 5.0:

                    abnormal_values += 1

                    abnormal_tests.append(
                        "T4"
                    )


        except ValueError:

            return jsonify({

                "success": False,

                "message":
                    "Please enter valid numerical values for TSH, T3 and T4."

            }), 400


        # ========================================================
        # GENERATE PERSONALIZED RESULT
        # ========================================================

        if (
            abnormal_values >= 2
            and symptom_count >= 3
        ):

            result = (
                "Your current information contains "
                "multiple thyroid-related laboratory "
                "reference indicators along with "
                "several selected symptoms. "
                "The symptoms selected include: "
                + ", ".join(selected_symptoms)
                + ". These recorded factors may "
                "warrant further evaluation by a "
                "qualified healthcare professional."
            )


        elif abnormal_values >= 2:

            result = (
                "Some of the thyroid laboratory "
                "values entered fall outside the "
                "reference thresholds used by this "
                "screening logic. "
                "The selected symptoms were: "
                + (
                    ", ".join(selected_symptoms)
                    if selected_symptoms
                    else "None"
                )
                + ". Further evaluation may "
                "be appropriate."
            )


        elif (
            abnormal_values == 1
            and symptom_count >= 3
        ):

            result = (
                "Your current information contains "
                "one thyroid-related laboratory "
                "reference indicator and several "
                "selected symptoms. "
                "The symptoms selected include: "
                + ", ".join(selected_symptoms)
                + ". These recorded factors may "
                "warrant further evaluation."
            )


        elif (
            abnormal_values == 1
            and symptom_count > 0
        ):

            result = (
                "One thyroid-related laboratory "
                "reference indicator was identified "
                "along with the following selected "
                "symptoms: "
                + ", ".join(selected_symptoms)
                + ". Consider discussing persistent "
                "or concerning symptoms with a "
                "healthcare professional."
            )


        elif abnormal_values == 1:

            result = (
                "One thyroid-related laboratory "
                "reference indicator was identified "
                "from the values entered. "
                "Further clinical evaluation may "
                "be appropriate."
            )


        elif symptom_count >= 5:

            result = (
                "You selected several thyroid-related "
                "symptoms: "
                + ", ".join(selected_symptoms)
                + ". These recorded factors may "
                "warrant further evaluation, "
                "especially if the symptoms are "
                "persistent or worsening."
            )


        elif symptom_count >= 3:

            result = (
                "Several thyroid-related symptoms "
                "were selected: "
                + ", ".join(selected_symptoms)
                + ". These recorded factors may "
                "warrant further evaluation if "
                "they persist."
            )


        elif symptom_count > 0:

            result = (
                "The following thyroid-related "
                "symptom was selected in your "
                "current profile: "
                + ", ".join(selected_symptoms)
                + ". Continue monitoring these "
                "symptoms and consider professional "
                "evaluation if they persist."
            )


        else:

            result = (
                "Your current responses contain "
                "few thyroid-related indicators. "
                "No thyroid-related symptoms were "
                "selected and no laboratory reference "
                "indicators were identified from "
                "the values provided."
            )


        # ========================================================
        # SAVE RESULT
        # ========================================================

        cursor.execute(
            """
            INSERT INTO thyroid_logs
            (
                user_id,
                tsh,
                t3,
                t4,
                fatigue,
                weight_change,
                cold_sensitivity,
                heat_sensitivity,
                hair_changes,
                mood_changes,
                sleep_problems,
                thyroid_result
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
                %s
            )
            """,
            (
                user_id,
                tsh if tsh not in ("", None) else None,
                t3 if t3 not in ("", None) else None,
                t4 if t4 not in ("", None) else None,

                fatigue,
                weight_change,
                cold_sensitivity,
                heat_sensitivity,
                hair_changes,
                mood_changes,
                sleep_problems,

                result
            )
        )


        connection.commit()


        # ========================================================
        # RESPONSE
        # ========================================================

        return jsonify({

            "success": True,

            "user_id": user_id,

            "symptom_count":
                symptom_count,

            "selected_symptoms":
                selected_symptoms,

            "abnormal_values":
                abnormal_values,

            "abnormal_tests":
                abnormal_tests,

            "result":
                result,

            "medical_notice":
                "This is a reference screening result based on the information provided and is not a medical diagnosis."

        }), 200


    # ============================================================
    # ERROR
    # ============================================================

    except Exception as error:

        if connection:

            connection.rollback()


        print(
            "========================================"
        )

        print(
            "THYROID ANALYSIS ERROR"
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

            "success": False,

            "message":
                "Unable to analyze thyroid data.",

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