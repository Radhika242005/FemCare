from backend.database import get_db_connection
from backend.services.menstrual_dataset_service import (
    get_personalized_menstrual_analysis
)


# ============================================================
# ANALYZE USER DATA
# ============================================================

def analyze_user_data(user_id):

    # ========================================================
    # GET PERSONALIZED CSV DATASET ANALYSIS
    # ========================================================

    dataset_analysis = (
        get_personalized_menstrual_analysis(
            user_id
        )
    )


    # ========================================================
    # GET USER PERIOD HISTORY
    # ========================================================

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute(
        """
        SELECT
            id,
            cycle_number,
            start_date,
            cycle_length_days,
            pain_level,
            pms_symptoms,
            mood_score,
            stress_score_cycle,
            sleep_hours_cycle,
            energy_level,
            concentration_score,
            work_hours_lost

        FROM period_logs

        WHERE user_id = %s

        ORDER BY start_date DESC, id DESC

        LIMIT 5
        """,
        (user_id,)
    )

    history = cursor.fetchall()

    cursor.close()
    connection.close()


    # ========================================================
    # NO PERIOD DATA
    # ========================================================

    if not history:

        return {

            "data_source":
                "none",

            "problems":
                [],

            "history_available":
                False,

            "history_cycles":
                0,

            "dataset_used":
                False

        }


    # ========================================================
    # CURRENT CYCLE
    # ========================================================

    latest = history[0]


    # ========================================================
    # FALLBACK FIELDS
    # ========================================================

    fallback_fields = [

        "cycle_length_days",

        "pain_level",

        "pms_symptoms",

        "mood_score",

        "stress_score_cycle",

        "sleep_hours_cycle",

        "energy_level",

        "concentration_score",

        "work_hours_lost"

    ]


    # ========================================================
    # KEEP TRACK OF FALLBACK SOURCES
    # ========================================================

    fallback_sources = {}

    used_previous_cycle = False

    used_older_cycle = False


    # ========================================================
    # FIELD-BY-FIELD FALLBACK
    #
    # Current cycle
    #      ↓
    # Previous cycle
    #      ↓
    # Older cycles
    # ========================================================

    for field in fallback_fields:

        # ----------------------------------------------------
        # Current value already exists
        # ----------------------------------------------------

        if latest.get(field) is not None:

            fallback_sources[field] = (
                "current_cycle"
            )

            continue


        # ----------------------------------------------------
        # Current value missing
        # Search older cycles
        # ----------------------------------------------------

        value_found = False


        for index in range(
            1,
            len(history)
        ):

            older_cycle = history[index]


            if (
                older_cycle.get(field)
                is not None
            ):

                latest[field] = (
                    older_cycle[field]
                )


                # --------------------------------------------
                # Record where the value came from
                # --------------------------------------------

                if index == 1:

                    fallback_sources[field] = (
                        "previous_cycle"
                    )

                    used_previous_cycle = True

                else:

                    fallback_sources[field] = (
                        "older_cycle"
                    )

                    used_older_cycle = True


                value_found = True

                break


        # ----------------------------------------------------
        # Nothing found in user history
        # ----------------------------------------------------

        if not value_found:

            fallback_sources[field] = (
                "not_available"
            )


    # ========================================================
    # DETERMINE DATA SOURCE
    # ========================================================

    if used_older_cycle:

        data_source = (
            "current_period_with_history_fallback"
        )

    elif used_previous_cycle:

        data_source = (
            "current_period_with_previous_fallback"
        )

    else:

        data_source = (
            "current_period"
        )


    # ========================================================
    # PROBLEM DETECTION
    # ========================================================

    problems = []


    # ========================================================
    # RULE 1 — HIGH STRESS
    # ========================================================

    if (

        latest["stress_score_cycle"]
        is not None

        and

        float(
            latest[
                "stress_score_cycle"
            ]
        ) >= 7

    ):

        problems.append(
            "High Stress"
        )


    # ========================================================
    # RULE 2 — POOR SLEEP
    # ========================================================

    if (

        latest["sleep_hours_cycle"]
        is not None

        and

        float(
            latest[
                "sleep_hours_cycle"
            ]
        ) < 6

    ):

        problems.append(
            "Poor Sleep"
        )


    # ========================================================
    # RULE 3 — PERIOD DISCOMFORT
    # ========================================================

    if (

        latest["pain_level"]
        is not None

        and

        int(
            latest[
                "pain_level"
            ]
        ) >= 5

    ):

        problems.append(
            "Period Discomfort"
        )


    # ========================================================
    # RULE 4 — LOW ENERGY
    # ========================================================

    if (

        latest["energy_level"]
        is not None

        and

        int(
            latest[
                "energy_level"
            ]
        ) <= 4

    ):

        problems.append(
            "Low Energy"
        )


    # ========================================================
    # RULE 5 — LOW MOOD
    # ========================================================

    if (

        latest["mood_score"]
        is not None

        and

        int(
            latest[
                "mood_score"
            ]
        ) <= 4

    ):

        problems.append(
            "Low Mood"
        )


    # ========================================================
    # RULE 6 — LOW CONCENTRATION
    # ========================================================

    if (

        latest["concentration_score"]
        is not None

        and

        int(
            latest[
                "concentration_score"
            ]
        ) <= 4

    ):

        problems.append(
            "Low Concentration"
        )


    # ========================================================
    # DATASET COMPARISON
    # ========================================================

    similar_patterns = (

        dataset_analysis.get(
            "similar_period_patterns",
            {}
        )

    )


    dataset_comparison = {}


    if similar_patterns:

        # ====================================================
        # STRESS
        # ====================================================

        if (

            latest[
                "stress_score_cycle"
            ] is not None

            and

            similar_patterns.get(
                "average_stress"
            ) is not None

        ):

            user_value = float(
                latest[
                    "stress_score_cycle"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_stress"
                ]
            )

            dataset_comparison[
                "stress"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


        # ====================================================
        # SLEEP
        # ====================================================

        if (

            latest[
                "sleep_hours_cycle"
            ] is not None

            and

            similar_patterns.get(
                "average_sleep"
            ) is not None

        ):

            user_value = float(
                latest[
                    "sleep_hours_cycle"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_sleep"
                ]
            )

            dataset_comparison[
                "sleep"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


        # ====================================================
        # PAIN
        # ====================================================

        if (

            latest[
                "pain_level"
            ] is not None

            and

            similar_patterns.get(
                "average_pain"
            ) is not None

        ):

            user_value = float(
                latest[
                    "pain_level"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_pain"
                ]
            )

            dataset_comparison[
                "pain"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


        # ====================================================
        # ENERGY
        # ====================================================

        if (

            latest[
                "energy_level"
            ] is not None

            and

            similar_patterns.get(
                "average_energy"
            ) is not None

        ):

            user_value = float(
                latest[
                    "energy_level"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_energy"
                ]
            )

            dataset_comparison[
                "energy"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


        # ====================================================
        # MOOD
        # ====================================================

        if (

            latest[
                "mood_score"
            ] is not None

            and

            similar_patterns.get(
                "average_mood"
            ) is not None

        ):

            user_value = float(
                latest[
                    "mood_score"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_mood"
                ]
            )

            dataset_comparison[
                "mood"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


        # ====================================================
        # CONCENTRATION
        # ====================================================

        if (

            latest[
                "concentration_score"
            ] is not None

            and

            similar_patterns.get(
                "average_concentration"
            ) is not None

        ):

            user_value = float(
                latest[
                    "concentration_score"
                ]
            )

            reference_value = float(
                similar_patterns[
                    "average_concentration"
                ]
            )

            dataset_comparison[
                "concentration"
            ] = {

                "user_value":
                    user_value,

                "reference_value":
                    reference_value,

                "difference":
                    round(
                        user_value -
                        reference_value,
                        2
                    )

            }


    # ========================================================
    # RETURN ANALYSIS
    # ========================================================

    return {

        "data_source":
            data_source,

        "cycle_number":
            latest[
                "cycle_number"
            ],

        "problems":
            problems,

        "data":
            latest,

        "history_available":
            len(history) > 1,

        "history_cycles":
            len(history),

        "used_previous_cycle":
            used_previous_cycle,

        "used_older_cycle":
            used_older_cycle,

        "fallback_sources":
            fallback_sources,

        "dataset_used":
            True,

        "similar_dataset_users":
            dataset_analysis.get(
                "similar_dataset_users",
                0
            ),

        "dataset_period_records_used":
            dataset_analysis.get(
                "dataset_period_records_used",
                0
            ),

        "dataset_comparison":
            dataset_comparison

    }