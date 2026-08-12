from flask import Blueprint, request, jsonify

from database import get_db_connection


periods_bp = Blueprint(
    "periods",
    __name__
)


# ============================================================
# SAVE PERIOD DATA
# ============================================================

@periods_bp.route(
    "",
    methods=["POST"]
)
def save_period():

    try:

        data = request.get_json()


        if not data:

            return jsonify({
                "message":
                    "No data received."
            }), 400


        # ----------------------------------------------------
        # GET USER ID
        # ----------------------------------------------------

        user_id = data.get(
            "user_id"
        )

        start_date = data.get(
            "start_date"
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not user_id:

            return jsonify({
                "message":
                    "User ID is required."
            }), 400


        if not start_date:

            return jsonify({
                "message":
                    "Period start date is required."
            }), 400


        # ----------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()


        # ====================================================
        # INSERT NEW PERIOD
        # ====================================================
        #
        # We initially store cycle_number as 0.
        # After insertion, all cycles are recalculated
        # chronologically.
        #
        # ====================================================

        cursor.execute(
            """
            INSERT INTO period_logs
            (
                user_id,
                cycle_number,
                start_date,
                cycle_length_days,
                prev_cycle_length,
                flow_level,
                pain_level,
                pms_symptoms,
                mood_score,
                stress_score_cycle,
                sleep_hours_cycle,
                energy_level,
                concentration_score,
                work_hours_lost,
                prepared_before_period
            )

            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            """,

            (
                user_id,

                0,

                start_date,

                data.get(
                    "cycle_length_days"
                ),

                None,

                data.get(
                    "flow_level"
                ),

                data.get(
                    "pain_level"
                ),

                data.get(
                    "pms_symptoms"
                ),

                data.get(
                    "mood_score"
                ),

                data.get(
                    "stress_score_cycle"
                ),

                data.get(
                    "sleep_hours_cycle"
                ),

                data.get(
                    "energy_level"
                ),

                data.get(
                    "concentration_score"
                ),

                data.get(
                    "work_hours_lost"
                ),

                data.get(
                    "prepared_before_period"
                )
            )
        )


        # ====================================================
        # REBUILD CYCLE NUMBERS CHRONOLOGICALLY
        # ====================================================

        cursor.execute(
            """
            SELECT
                id,
                cycle_length_days,
                start_date

            FROM period_logs

            WHERE user_id = %s

            ORDER BY
                start_date ASC,
                id ASC
            """,

            (user_id,)
        )


        all_cycles = cursor.fetchall()


        # ====================================================
        # ASSIGN CYCLE NUMBERS
        # ====================================================

        cycle_number = 1

        previous_cycle_length = None


        for cycle in all_cycles:

            record_id = cycle[0]

            current_cycle_length = cycle[1]


            cursor.execute(
                """
                UPDATE period_logs

                SET
                    cycle_number = %s,
                    prev_cycle_length = %s

                WHERE id = %s
                """,

                (
                    cycle_number,
                    previous_cycle_length,
                    record_id
                )
            )


            # Current cycle becomes previous cycle
            # for the next chronological record.

            previous_cycle_length = (
                current_cycle_length
            )


            cycle_number += 1


        # ====================================================
        # COMMIT
        # ====================================================

        connection.commit()


        # ====================================================
        # FIND THE CYCLE NUMBER OF THE RECORD JUST INSERTED
        # ====================================================

        cursor.execute(
            """
            SELECT
                cycle_number

            FROM period_logs

            WHERE user_id = %s
              AND start_date = %s

            ORDER BY id DESC

            LIMIT 1
            """,

            (
                user_id,
                start_date
            )
        )


        inserted_record = cursor.fetchone()


        if inserted_record:

            new_cycle_number = (
                inserted_record[0]
            )

        else:

            new_cycle_number = None


        # ====================================================
        # CLOSE CONNECTION
        # ====================================================

        cursor.close()

        connection.close()


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "message":
                "Period data saved successfully.",

            "cycle_number":
                new_cycle_number

        }), 201


    except Exception as error:

        print(
            "Period error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Server error while saving period data."

        }), 500


# ============================================================
# GET PERIOD HISTORY
# ============================================================

@periods_bp.route(
    "/history/<int:user_id>",
    methods=["GET"]
)
def get_period_history(user_id):

    try:

        # ----------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ----------------------------------------------------
        # GET USER PERIOD HISTORY
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                cycle_number,
                start_date,
                cycle_length_days,
                prev_cycle_length,
                cycle_phase,
                flow_level,
                pain_level,
                pms_symptoms,
                mood_score,
                stress_score_cycle,
                sleep_hours_cycle,
                energy_level,
                concentration_score,
                work_hours_lost,
                overall_health_score,
                log_consistency_score,
                prepared_before_period,
                created_at

            FROM period_logs

            WHERE user_id = %s

            ORDER BY
                start_date DESC,
                id DESC
            """,

            (user_id,)
        )


        history = cursor.fetchall()


        # ----------------------------------------------------
        # CLOSE CONNECTION
        # ----------------------------------------------------

        cursor.close()

        connection.close()


        # ----------------------------------------------------
        # RETURN HISTORY
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "history":
                history

        }), 200


    except Exception as error:

        print(
            "History error:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Unable to load period history."

        }), 500


# ============================================================
# PERIOD TREND ANALYSIS
# ============================================================

@periods_bp.route(
    "/trend/<int:user_id>",
    methods=["GET"]
)
def get_period_trend(user_id):

    try:

        # ----------------------------------------------------
        # DATABASE CONNECTION
        # ----------------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ----------------------------------------------------
        # GET LAST 5 CHRONOLOGICAL CYCLES
        #
        # We use multiple cycles because a value may be
        # missing in the latest cycle AND previous cycle.
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                cycle_number,
                start_date,
                cycle_length_days,
                pain_level,
                mood_score,
                stress_score_cycle,
                sleep_hours_cycle,
                energy_level,
                concentration_score

            FROM period_logs

            WHERE user_id = %s

            ORDER BY
                start_date DESC,
                id DESC

            LIMIT 5
            """,

            (user_id,)
        )


        cycles = cursor.fetchall()


        cursor.close()

        connection.close()


        # ----------------------------------------------------
        # NOT ENOUGH DATA
        # ----------------------------------------------------

        if len(cycles) < 2:

            return jsonify({

                "success": True,

                "message":
                    "At least two cycles are required for trend analysis.",

                "trend_available":
                    False,

                "cycles":
                    cycles

            }), 200


        # ----------------------------------------------------
        # LATEST CYCLE
        # ----------------------------------------------------

        latest = cycles[0]


        # ----------------------------------------------------
        # PREVIOUS CYCLE
        # ----------------------------------------------------

        previous = cycles[1]


        # ----------------------------------------------------
        # CREATE COPIES
        #
        # We don't modify the original database records.
        # ----------------------------------------------------

        latest_display = dict(
            latest
        )

        previous_display = dict(
            previous
        )


        # ====================================================
        # TREND FIELDS
        # ====================================================

        trend_fields = {

            "pain":
                "pain_level",

            "mood":
                "mood_score",

            "stress":
                "stress_score_cycle",

            "sleep":
                "sleep_hours_cycle",

            "energy":
                "energy_level",

            "concentration":
                "concentration_score",

            "cycle_length":
                "cycle_length_days"

        }


        # ====================================================
        # FALLBACK FUNCTION
        # ====================================================

        def get_value_with_fallback(
            field,
            starting_index
        ):

            # ------------------------------------------------
            # Check requested cycle first.
            # ------------------------------------------------

            current_value = (
                cycles[starting_index].get(
                    field
                )
            )


            if current_value is not None:

                if starting_index == 0:

                    source = "current_cycle"

                elif starting_index == 1:

                    source = "previous_cycle"

                else:

                    source = "older_cycle"


                return {

                    "value":
                        current_value,

                    "source":
                        source

                }


            # ------------------------------------------------
            # Search older cycles.
            # ------------------------------------------------

            for index in range(
                starting_index + 1,
                len(cycles)
            ):

                older_value = (
                    cycles[index].get(
                        field
                    )
                )


                if older_value is not None:

                    if index == 1:

                        source = "previous_cycle"

                    else:

                        source = "older_cycle"


                    return {

                        "value":
                            older_value,

                        "source":
                            source

                    }


            # ------------------------------------------------
            # Nothing available.
            # ------------------------------------------------

            return {

                "value":
                    None,

                "source":
                    "not_available"

            }


        # ====================================================
        # FALLBACK SOURCES
        # ====================================================

        fallback_sources = {}


        # ====================================================
        # CALCULATE TRENDS
        # ====================================================

        trend = {}


        # ====================================================
        # COMPARE VALUES
        # ====================================================

        def compare_values(
            latest_value,
            previous_value
        ):

            # ------------------------------------------------
            # Missing data
            # ------------------------------------------------

            if (
                latest_value is None
                or
                previous_value is None
            ):

                return {

                    "status":
                        "insufficient_data",

                    "change":
                        None

                }


            # ------------------------------------------------
            # Convert numeric values
            # ------------------------------------------------

            latest_value = float(
                latest_value
            )


            previous_value = float(
                previous_value
            )


            # ------------------------------------------------
            # Calculate difference
            # ------------------------------------------------

            difference = (
                latest_value
                -
                previous_value
            )


            # ------------------------------------------------
            # Determine status
            # ------------------------------------------------

            if difference > 0:

                status = "increased"

            elif difference < 0:

                status = "decreased"

            else:

                status = "unchanged"


            return {

                "status":
                    status,

                "change":
                    round(
                        difference,
                        2
                    )

            }


        # ====================================================
        # PROCESS EACH FIELD
        # ====================================================

        for trend_name, field in trend_fields.items():

            # ------------------------------------------------
            # GET LATEST VALUE
            #
            # Current cycle → previous → older
            # ------------------------------------------------

            latest_result = (
                get_value_with_fallback(
                    field,
                    0
                )
            )


            # ------------------------------------------------
            # GET PREVIOUS VALUE
            #
            # Previous cycle → older
            # ------------------------------------------------

            previous_result = (
                get_value_with_fallback(
                    field,
                    1
                )
            )


            latest_value = (
                latest_result["value"]
            )


            previous_value = (
                previous_result["value"]
            )


            # ------------------------------------------------
            # SAVE FALLBACK INFORMATION
            # ------------------------------------------------

            fallback_sources[
                trend_name
            ] = {

                "latest":
                    latest_result["source"],

                "previous":
                    previous_result["source"]

            }


            # ------------------------------------------------
            # Update values returned to frontend
            #
            # This prevents null → 0 in JavaScript.
            # ------------------------------------------------

            latest_display[
                field
            ] = latest_value


            previous_display[
                field
            ] = previous_value


            # ------------------------------------------------
            # CALCULATE TREND
            # ------------------------------------------------

            trend[
                trend_name
            ] = compare_values(
                latest_value,
                previous_value
            )


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return jsonify({

            "success":
                True,

            "trend_available":
                True,

            "latest_cycle":
                latest_display,

            "previous_cycle":
                previous_display,

            "trend":
                trend,

            "fallback_sources":
                fallback_sources

        }), 200


    except Exception as error:

        print(
            "Trend error:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Unable to calculate period trends."

        }), 500