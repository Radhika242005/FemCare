from flask import Blueprint, request, jsonify
from database import get_db_connection

perimenopause_bp = Blueprint(
    "perimenopause",
    __name__
)


@perimenopause_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_perimenopause():

    connection = None
    cursor = None

    try:

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

        if age < 35 or age > 70:
            return jsonify({
                "success": False,
                "message": "Age must be between 35 and 70."
            }), 400


        # ========================================================
        # GET SYMPTOMS
        # ========================================================

        cycle_irregularity = data.get(
            "cycle_irregularity"
        )

        hot_flashes = data.get(
            "hot_flashes"
        )

        night_sweats = data.get(
            "night_sweats"
        )

        mood_changes = data.get(
            "mood_changes"
        )

        sleep_problems = data.get(
            "sleep_problems"
        )

        vaginal_dryness = data.get(
            "vaginal_dryness"
        )

        fatigue = data.get(
            "fatigue"
        )

        headache = data.get(
            "headache"
        )

        concentration_problems = data.get(
            "concentration_problems"
        )


        # ========================================================
        # SYMPTOM DICTIONARY
        # ========================================================

        symptoms = {

            "Cycle irregularity":
                cycle_irregularity,

            "Hot flashes":
                hot_flashes,

            "Night sweats":
                night_sweats,

            "Mood changes":
                mood_changes,

            "Sleep problems":
                sleep_problems,

            "Vaginal dryness":
                vaginal_dryness,

            "Fatigue":
                fatigue,

            "Headache":
                headache,

            "Concentration problems":
                concentration_problems
        }


        # ========================================================
        # FIND SELECTED SYMPTOMS
        # ========================================================

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
        # PERSONALIZED RESULT
        # ========================================================

        # Age 45+ with many symptoms
        if age >= 45 and symptom_count >= 6:

            result = (
                f"At age {age}, several symptoms were "
                f"selected that can occur during the "
                f"perimenopause transition. The selected "
                f"symptoms are: "
                f"{', '.join(selected_symptoms)}. "
                f"The combination of these reported "
                f"symptoms may warrant further discussion "
                f"with a qualified healthcare professional."
            )


        # Age 40-44 with many symptoms
        elif age >= 40 and symptom_count >= 6:

            result = (
                f"At age {age}, multiple symptoms were "
                f"selected: "
                f"{', '.join(selected_symptoms)}. "
                f"These recorded symptoms may be associated "
                f"with hormonal or menstrual changes and "
                f"may warrant further evaluation."
            )


        # Age 40+ with 4-5 symptoms
        elif age >= 40 and symptom_count >= 4:

            result = (
                f"At age {age}, {symptom_count} symptoms "
                f"were selected: "
                f"{', '.join(selected_symptoms)}. "
                f"The current information contains several "
                f"perimenopause-related reference indicators."
            )


        # Age 40+ with 2-3 symptoms
        elif age >= 40 and symptom_count >= 2:

            result = (
                f"At age {age}, the following symptoms "
                f"were selected: "
                f"{', '.join(selected_symptoms)}. "
                f"Some perimenopause-related reference "
                f"indicators are present in the information "
                f"provided."
            )


        # Age 40+ with one symptom
        elif age >= 40 and symptom_count == 1:

            result = (
                f"At age {age}, one symptom was selected: "
                f"{selected_symptoms[0]}. "
                f"The current information contains a limited "
                f"number of perimenopause-related indicators."
            )


        # Age 40+ with no symptoms
        elif age >= 40 and symptom_count == 0:

            result = (
                f"At age {age}, no perimenopause-related "
                f"symptoms were selected. The current "
                f"information does not show strong "
                f"perimenopause reference indicators."
            )


        # Age below 40 with many symptoms
        elif age < 40 and symptom_count >= 5:

            result = (
                f"At age {age}, several symptoms were "
                f"selected: "
                f"{', '.join(selected_symptoms)}. "
                f"Although the selected age is below the "
                f"usual age range considered by this "
                f"reference screening, the reported "
                f"symptoms may still warrant professional "
                f"evaluation."
            )


        # Age below 40 with some symptoms
        elif age < 40 and symptom_count >= 2:

            result = (
                f"At age {age}, the following symptoms "
                f"were selected: "
                f"{', '.join(selected_symptoms)}. "
                f"The current information contains some "
                f"symptoms that may require monitoring "
                f"or further discussion with a healthcare "
                f"professional."
            )


        # Age below 40 with one symptom
        elif age < 40 and symptom_count == 1:

            result = (
                f"At age {age}, one symptom was selected: "
                f"{selected_symptoms[0]}. "
                f"The current information does not show "
                f"multiple perimenopause reference indicators."
            )


        # Age below 40 with no symptoms
        else:

            result = (
                f"At age {age}, no perimenopause-related "
                f"symptoms were selected. The current "
                f"information does not show strong "
                f"perimenopause reference indicators."
            )


        # ========================================================
        # DATABASE
        # ========================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            INSERT INTO perimenopause_logs
            (
                user_id,
                age,
                cycle_irregularity,
                hot_flashes,
                night_sweats,
                mood_changes,
                sleep_problems,
                vaginal_dryness,
                fatigue,
                headache,
                concentration_problems,
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
                %s
            )
            """,
            (
                user_id,
                age,
                cycle_irregularity,
                hot_flashes,
                night_sweats,
                mood_changes,
                sleep_problems,
                vaginal_dryness,
                fatigue,
                headache,
                concentration_problems,
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

            "symptom_count":
                symptom_count,

            "selected_symptoms":
                selected_symptoms,

            "result":
                result,

            "medical_notice":
                "This is a reference screening result based on the information provided and is not a medical diagnosis."

        }), 200


    except Exception as error:

        if connection:
            connection.rollback()


        print(
            "========================================"
        )

        print(
            "PERIMENOPAUSE ANALYSIS ERROR"
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
                "Unable to analyze perimenopause data.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()