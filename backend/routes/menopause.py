from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

menopause_bp = Blueprint(
    "menopause",
    __name__
)


@menopause_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_menopause():

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

        if age < 35 or age > 100:
            return jsonify({
                "success": False,
                "message": "Age must be between 35 and 100."
            }), 400


        # ========================================================
        # MENSTRUAL INFORMATION
        # ========================================================

        periods_stopped = data.get(
            "periods_stopped"
        )

        months_since_last_period = data.get(
            "months_since_last_period"
        )


        if months_since_last_period in (
            None,
            ""
        ):

            months_since_last_period = 0

        else:

            try:

                months_since_last_period = int(
                    months_since_last_period
                )

            except (ValueError, TypeError):

                return jsonify({
                    "success": False,
                    "message":
                        "Months since last period must be a valid number."
                }), 400


        if months_since_last_period < 0:

            return jsonify({
                "success": False,
                "message":
                    "Months since last period cannot be negative."
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

        concentration_problems = data.get(
            "concentration_problems"
        )

        joint_pain = data.get(
            "joint_pain"
        )


        # ========================================================
        # SYMPTOM DICTIONARY
        # ========================================================

        symptoms = {

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

            "Concentration problems":
                concentration_problems,

            "Joint pain":
                joint_pain
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
        # MENSTRUAL STATUS
        # ========================================================

        twelve_month_pattern = (
            str(periods_stopped).strip().lower() == "yes"
            and months_since_last_period >= 12
        )


        # ========================================================
        # PERSONALIZED REFERENCE RESULT
        # ========================================================

        # --------------------------------------------------------
        # 12+ MONTHS WITHOUT PERIOD
        # --------------------------------------------------------

        if twelve_month_pattern:

            if symptom_count >= 5:

                result = (
                    f"At age {age}, the reported information "
                    f"shows that periods have stopped and "
                    f"{months_since_last_period} months have "
                    f"passed since the last period. "
                    f"The selected symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"This information shows a menopause-stage "
                    f"reference pattern with several associated "
                    f"symptoms."
                )

            elif symptom_count >= 2:

                result = (
                    f"At age {age}, periods have been reported "
                    f"as stopped for {months_since_last_period} "
                    f"months. The selected symptoms are: "
                    f"{', '.join(selected_symptoms)}. "
                    f"The information is consistent with a "
                    f"menopause-stage reference pattern and "
                    f"includes some associated symptoms."
                )

            elif symptom_count == 1:

                result = (
                    f"At age {age}, periods have been reported "
                    f"as stopped for {months_since_last_period} "
                    f"months. The selected symptom is "
                    f"{selected_symptoms[0]}. "
                    f"The menstrual information shows a "
                    f"menopause-stage reference pattern."
                )

            else:

                result = (
                    f"At age {age}, periods have been reported "
                    f"as stopped for {months_since_last_period} "
                    f"months. No common menopause-related "
                    f"symptoms were selected. The menstrual "
                    f"information shows a menopause-stage "
                    f"reference pattern."
                )


        # --------------------------------------------------------
        # PERIODS NOT STOPPED + MANY SYMPTOMS
        # --------------------------------------------------------

        elif symptom_count >= 6:

            result = (
                f"At age {age}, periods have not been reported "
                f"as stopped for 12 months. However, several "
                f"symptoms were selected: "
                f"{', '.join(selected_symptoms)}. "
                f"The reported information contains multiple "
                f"menopause-related reference indicators, "
                f"although the menstrual information does not "
                f"show a 12-month period-free pattern."
            )


        # --------------------------------------------------------
        # PERIODS NOT STOPPED + 4-5 SYMPTOMS
        # --------------------------------------------------------

        elif symptom_count >= 4:

            result = (
                f"At age {age}, the following symptoms were "
                f"selected: "
                f"{', '.join(selected_symptoms)}. "
                f"Several menopause-related reference "
                f"indicators are present, but the reported "
                f"menstrual information does not show "
                f"12 months without a period."
            )


        # --------------------------------------------------------
        # PERIODS NOT STOPPED + 2-3 SYMPTOMS
        # --------------------------------------------------------

        elif symptom_count >= 2:

            result = (
                f"At age {age}, the following symptoms were "
                f"selected: "
                f"{', '.join(selected_symptoms)}. "
                f"Some menopause-related reference indicators "
                f"are present. The menstrual information "
                f"should be considered together with the "
                f"reported symptoms."
            )


        # --------------------------------------------------------
        # ONE SYMPTOM
        # --------------------------------------------------------

        elif symptom_count == 1:

            result = (
                f"At age {age}, one symptom was selected: "
                f"{selected_symptoms[0]}. "
                f"The current information contains a limited "
                f"number of menopause-related reference "
                f"indicators."
            )


        # --------------------------------------------------------
        # NO SYMPTOMS
        # --------------------------------------------------------

        else:

            result = (
                f"At age {age}, no common menopause-related "
                f"symptoms were selected. The current "
                f"information does not show strong menopause "
                f"reference indicators."
            )


        # ========================================================
        # DATABASE CONNECTION
        # ========================================================

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ========================================================
        # SAVE RESULT
        # ========================================================

        cursor.execute(
            """
            INSERT INTO menopause_logs
            (
                user_id,
                age,
                periods_stopped,
                months_since_last_period,
                hot_flashes,
                night_sweats,
                mood_changes,
                sleep_problems,
                vaginal_dryness,
                fatigue,
                concentration_problems,
                joint_pain,
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
                age,
                periods_stopped,
                months_since_last_period,
                hot_flashes,
                night_sweats,
                mood_changes,
                sleep_problems,
                vaginal_dryness,
                fatigue,
                concentration_problems,
                joint_pain,
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

            "months_since_last_period":
                months_since_last_period,

            "symptom_count":
                symptom_count,

            "selected_symptoms":
                selected_symptoms,

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
            "MENOPAUSE ANALYSIS ERROR"
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
                "Unable to analyze menopause data.",

            "error":
                str(error)

        }), 500


    # ============================================================
    # CLOSE
    # ============================================================

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()