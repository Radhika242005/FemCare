from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

postmenopause_bp = Blueprint(
    "postmenopause",
    __name__
)


@postmenopause_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_postmenopause():

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


        if age < 40 or age > 100:
            return jsonify({
                "success": False,
                "message": "Age must be between 40 and 100."
            }), 400


        # ========================================================
        # YEARS SINCE MENOPAUSE
        # ========================================================

        years_since_menopause = data.get(
            "years_since_menopause"
        )

        if years_since_menopause in (None, ""):

            years_since_menopause = 0

        else:

            try:

                years_since_menopause = float(
                    years_since_menopause
                )

            except (ValueError, TypeError):

                return jsonify({
                    "success": False,
                    "message":
                        "Years since menopause must be a valid number."
                }), 400


        if years_since_menopause < 0:

            return jsonify({
                "success": False,
                "message":
                    "Years since menopause cannot be negative."
            }), 400


        # ========================================================
        # SYMPTOMS
        # ========================================================

        hot_flashes = data.get(
            "hot_flashes"
        )

        night_sweats = data.get(
            "night_sweats"
        )

        vaginal_dryness = data.get(
            "vaginal_dryness"
        )

        sleep_problems = data.get(
            "sleep_problems"
        )

        mood_changes = data.get(
            "mood_changes"
        )

        fatigue = data.get(
            "fatigue"
        )

        joint_pain = data.get(
            "joint_pain"
        )

        urinary_symptoms = data.get(
            "urinary_symptoms"
        )

        bone_health_concern = data.get(
            "bone_health_concern"
        )

        concentration_problems = data.get(
            "concentration_problems"
        )


        # ========================================================
        # SYMPTOM DICTIONARY
        # ========================================================

        symptoms = {

            "Hot flashes":
                hot_flashes,

            "Night sweats":
                night_sweats,

            "Vaginal dryness":
                vaginal_dryness,

            "Sleep problems":
                sleep_problems,

            "Mood changes":
                mood_changes,

            "Fatigue":
                fatigue,

            "Joint pain":
                joint_pain,

            "Urinary symptoms":
                urinary_symptoms,

            "Bone health concern":
                bone_health_concern,

            "Concentration problems":
                concentration_problems
        }


        # ========================================================
        # SELECTED SYMPTOMS
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
        # POSTMENOPAUSE REFERENCE LOGIC
        # ========================================================

        if (
            age >= 50
            and years_since_menopause >= 1
        ):

            if symptom_count >= 7:

                result = (
                    f"At age {age}, the reported information "
                    f"indicates approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause. The selected symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"Several postmenopause-related indicators "
                    f"are present in the information provided."
                )

            elif symptom_count >= 4:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"The information contains several "
                    f"postmenopause-related reference indicators."
                )

            elif symptom_count >= 2:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"Some postmenopause-related reference "
                    f"indicators are present."
                )

            elif symptom_count == 1:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptom is: "
                    f"{selected_symptoms[0]}. "
                    f"The information contains a limited "
                    f"number of postmenopause-related indicators."
                )

            else:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. No postmenopause-"
                    f"related symptoms were selected. The current "
                    f"information does not show strong symptom-"
                    f"related reference indicators."
                )


        elif age >= 50 and years_since_menopause < 1:

            if symptom_count >= 5:

                result = (
                    f"At age {age}, several symptoms were "
                    f"selected: "
                    f"{', '.join(selected_symptoms)}. "
                    f"However, less than one year since menopause "
                    f"was reported, so the information does not "
                    f"represent a strong postmenopause-stage "
                    f"reference profile."
                )

            elif symptom_count >= 2:

                result = (
                    f"At age {age}, the selected symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"Some menopause-related symptoms are "
                    f"present, but less than one year since "
                    f"menopause was reported."
                )

            elif symptom_count == 1:

                result = (
                    f"At age {age}, the selected symptom is "
                    f"{selected_symptoms[0]}. "
                    f"The current information does not show "
                    f"a strong postmenopause-stage reference "
                    f"profile."
                )

            else:

                result = (
                    f"At age {age}, no postmenopause-related "
                    f"symptoms were selected and less than "
                    f"one year since menopause was reported. "
                    f"The current information does not show "
                    f"strong postmenopause reference indicators."
                )


        elif age < 50 and years_since_menopause >= 1:

            if symptom_count >= 4:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"Several postmenopause-related indicators "
                    f"are present, although the selected age "
                    f"is below 50."
                )

            elif symptom_count >= 2:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"Some postmenopause-related indicators "
                    f"are present."
                )

            elif symptom_count == 1:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. The selected "
                    f"symptom is "
                    f"{selected_symptoms[0]}. "
                    f"Limited postmenopause-related indicators "
                    f"are present."
                )

            else:

                result = (
                    f"At age {age}, approximately "
                    f"{years_since_menopause:g} year(s) since "
                    f"menopause were reported. No symptoms were "
                    f"selected. The information does not show "
                    f"strong symptom-related reference indicators."
                )


        else:

            if symptom_count >= 4:

                result = (
                    f"At age {age}, the following symptoms were "
                    f"selected: "
                    f"{', '.join(selected_symptoms)}. "
                    f"The reported information contains some "
                    f"symptoms that may require monitoring or "
                    f"further discussion with a healthcare "
                    f"professional."
                )

            elif symptom_count > 0:

                result = (
                    f"At age {age}, the following symptom(s) "
                    f"were selected: "
                    f"{', '.join(selected_symptoms)}. "
                    f"The current information does not show "
                    f"a strong postmenopause reference profile."
                )

            else:

                result = (
                    f"At age {age}, no postmenopause-related "
                    f"symptoms were selected. The current "
                    f"information does not show strong "
                    f"postmenopause reference indicators."
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
            INSERT INTO postmenopause_logs
            (
                user_id,
                age,
                years_since_menopause,
                hot_flashes,
                night_sweats,
                vaginal_dryness,
                sleep_problems,
                mood_changes,
                fatigue,
                joint_pain,
                urinary_symptoms,
                bone_health_concern,
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
                %s,
                %s,
                %s
            )
            """,
            (
                user_id,
                age,
                years_since_menopause,
                hot_flashes,
                night_sweats,
                vaginal_dryness,
                sleep_problems,
                mood_changes,
                fatigue,
                joint_pain,
                urinary_symptoms,
                bone_health_concern,
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

            "years_since_menopause":
                years_since_menopause,

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
            "POSTMENOPAUSE ANALYSIS ERROR"
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
                "Unable to analyze postmenopause data.",

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()