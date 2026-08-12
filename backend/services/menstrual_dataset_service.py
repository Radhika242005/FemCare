import os
import pandas as pd


# ============================================================
# DATASET PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


USER_PROFILE_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "menstrual",
    "cleaned",
    "User_Profile_cleaned.csv"
)


PERIOD_LOG_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "menstrual",
    "cleaned",
    "Period_Log_cleaned.csv"
)


# ============================================================
# LOAD USER PROFILE DATASET
# ============================================================

def load_user_profile_dataset():

    if not os.path.exists(
        USER_PROFILE_PATH
    ):

        raise FileNotFoundError(
            "User Profile dataset not found."
        )


    df = pd.read_csv(
        USER_PROFILE_PATH
    )

    return df


# ============================================================
# LOAD PERIOD LOG DATASET
# ============================================================

def load_period_log_dataset():

    if not os.path.exists(
        PERIOD_LOG_PATH
    ):

        raise FileNotFoundError(
            "Period Log dataset not found."
        )


    df = pd.read_csv(
        PERIOD_LOG_PATH
    )

    return df


# ============================================================
# DATASET SUMMARY
# ============================================================

def get_menstrual_dataset_summary():

    user_df = load_user_profile_dataset()

    period_df = load_period_log_dataset()


    return {

        "user_profile": {

            "rows":
                int(user_df.shape[0]),

            "columns":
                int(user_df.shape[1]),

            "column_names":
                list(user_df.columns)

        },


        "period_log": {

            "rows":
                int(period_df.shape[0]),

            "columns":
                int(period_df.shape[1]),

            "column_names":
                list(period_df.columns)

        }

    }
# ============================================================
# MENSTRUAL DATASET ANALYSIS
# ============================================================

def get_menstrual_dataset_analysis():

    user_df = load_user_profile_dataset()

    period_df = load_period_log_dataset()


    # --------------------------------------------------------
    # CONVERT NUMERIC COLUMNS
    # --------------------------------------------------------

    user_numeric_columns = [
        "age",
        "bmi",
        "sleep_hours",
        "water_intake_liters",
        "stress_score_baseline"
    ]


    period_numeric_columns = [
        "cycle_length_days",
        "pain_level",
        "mood_score",
        "stress_score_cycle",
        "sleep_hours_cycle",
        "energy_level",
        "concentration_score",
        "work_hours_lost",
        "overall_health_score",
        "log_consistency_score"
    ]


    for column in user_numeric_columns:

        if column in user_df.columns:

            user_df[column] = pd.to_numeric(
                user_df[column],
                errors="coerce"
            )


    for column in period_numeric_columns:

        if column in period_df.columns:

            period_df[column] = pd.to_numeric(
                period_df[column],
                errors="coerce"
            )


    # --------------------------------------------------------
    # USER PROFILE ANALYSIS
    # --------------------------------------------------------

    user_analysis = {

        "total_users":
            int(len(user_df)),

        "average_age":
            round(
                user_df["age"].mean(),
                2
            ),

        "average_bmi":
            round(
                user_df["bmi"].mean(),
                2
            ),

        "average_sleep_hours":
            round(
                user_df["sleep_hours"].mean(),
                2
            ),

        "average_water_intake":
            round(
                user_df["water_intake_liters"].mean(),
                2
            ),

        "average_baseline_stress":
            round(
                user_df["stress_score_baseline"].mean(),
                2
            )

    }


    # --------------------------------------------------------
    # PERIOD ANALYSIS
    # --------------------------------------------------------

    period_analysis = {

        "total_period_records":
            int(len(period_df)),

        "average_cycle_length":
            round(
                period_df[
                    "cycle_length_days"
                ].mean(),
                2
            ),

        "average_pain":
            round(
                period_df[
                    "pain_level"
                ].mean(),
                2
            ),

        "average_mood":
            round(
                period_df[
                    "mood_score"
                ].mean(),
                2
            ),

        "average_stress":
            round(
                period_df[
                    "stress_score_cycle"
                ].mean(),
                2
            ),

        "average_sleep":
            round(
                period_df[
                    "sleep_hours_cycle"
                ].mean(),
                2
            ),

        "average_energy":
            round(
                period_df[
                    "energy_level"
                ].mean(),
                2
            ),

        "average_concentration":
            round(
                period_df[
                    "concentration_score"
                ].mean(),
                2
            ),

        "average_work_hours_lost":
            round(
                period_df[
                    "work_hours_lost"
                ].mean(),
                2
            )

    }


    # --------------------------------------------------------
    # COMMON CATEGORICAL VALUES
    # --------------------------------------------------------

    flow_distribution = (
        period_df[
            "flow_level"
        ]
        .value_counts(
            dropna=True
        )
        .to_dict()
    )


    exercise_distribution = (
        user_df[
            "exercise_frequency"
        ]
        .value_counts(
            dropna=True
        )
        .to_dict()
    )


    diet_distribution = (
        user_df[
            "diet_quality"
        ]
        .value_counts(
            dropna=True
        )
        .to_dict()
    )


    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "user_profile": user_analysis,

        "period_log": period_analysis,

        "flow_distribution":
            flow_distribution,

        "exercise_distribution":
            exercise_distribution,

        "diet_distribution":
            diet_distribution

    }
def get_personalized_menstrual_analysis(user_id):

    from database import get_db_connection

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    # ========================================================
    # GET USER PROFILE FROM MYSQL
    # ========================================================

    cursor.execute(
        """
        SELECT
            age,
            bmi,
            diet_quality,
            exercise_frequency,
            sleep_hours,
            water_intake_liters,
            caffeine_intake,
            alcohol_consumption,
            smoking_status,
            birth_control_use,
            pcos_diagnosed,
            stress_score_baseline

        FROM health_profiles

        WHERE user_id = %s

        LIMIT 1
        """,
        (user_id,)
    )

    profile = cursor.fetchone()


    # ========================================================
    # GET LATEST PERIOD DATA FROM MYSQL
    # ========================================================

    cursor.execute(
        """
        SELECT
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

        LIMIT 1
        """,
        (user_id,)
    )

    period = cursor.fetchone()


    cursor.close()
    connection.close()


    # ========================================================
    # CHECK USER PROFILE
    # ========================================================

    if not profile:

        return {
            "success": False,
            "message": "Health profile not found."
        }


    # ========================================================
    # LOAD CSV DATASETS
    # ========================================================

    user_df = load_user_profile_dataset()

    period_df = load_period_log_dataset()


    # ========================================================
    # CONVERT NUMERIC COLUMNS
    # ========================================================

    numeric_profile_columns = [
        "age",
        "bmi",
        "sleep_hours",
        "water_intake_liters",
        "stress_score_baseline"
    ]

    for column in numeric_profile_columns:

        user_df[column] = pd.to_numeric(
            user_df[column],
            errors="coerce"
        )


    numeric_period_columns = [
        "cycle_length_days",
        "pain_level",
        "mood_score",
        "stress_score_cycle",
        "sleep_hours_cycle",
        "energy_level",
        "concentration_score",
        "work_hours_lost"
    ]

    for column in numeric_period_columns:

        period_df[column] = pd.to_numeric(
            period_df[column],
            errors="coerce"
        )


    # ========================================================
    # FIND SIMILAR PROFILE RECORDS
    # ========================================================

    profile_working = user_df.copy()

    profile_working["similarity_score"] = 0.0


    # Age similarity

    if profile.get("age") is not None:

        profile_working["similarity_score"] += (
            abs(
                profile_working["age"]
                - float(profile["age"])
            ) / 10
        )


    # BMI similarity

    if profile.get("bmi") is not None:

        profile_working["similarity_score"] += (
            abs(
                profile_working["bmi"]
                - float(profile["bmi"])
            ) / 5
        )


    # Sleep similarity

    if profile.get("sleep_hours") is not None:

        profile_working["similarity_score"] += (
            abs(
                profile_working["sleep_hours"]
                - float(profile["sleep_hours"])
            ) / 3
        )


    # Stress similarity

    if profile.get("stress_score_baseline") is not None:

        profile_working["similarity_score"] += (
            abs(
                profile_working[
                    "stress_score_baseline"
                ]
                - float(
                    profile[
                        "stress_score_baseline"
                    ]
                )
            ) / 3
        )


    # ========================================================
    # CATEGORICAL MATCHING
    # ========================================================

    categorical_fields = [
        "diet_quality",
        "exercise_frequency",
        "caffeine_intake",
        "alcohol_consumption",
        "smoking_status",
        "birth_control_use",
        "pcos_diagnosed"
    ]


    for field in categorical_fields:

        if profile.get(field) is not None:

            profile_working["similarity_score"] += (

                profile_working[field]
                .astype(str)
                .str.lower()
                !=
                str(
                    profile[field]
                ).lower()

            ).astype(float)


    # ========================================================
    # GET TOP 5 SIMILAR DATASET USERS
    # ========================================================

    similar_users = (
        profile_working
        .sort_values(
            "similarity_score"
        )
        .head(5)
    )


    # ========================================================
    # GET PERIOD RECORDS OF SIMILAR USERS
    # ========================================================

    similar_user_ids = (
        similar_users["user_id"]
        .tolist()
    )


    similar_periods = (
        period_df[
            period_df["user_id"].isin(
                similar_user_ids
            )
        ]
        .copy()
    )


    # ========================================================
    # CALCULATE RELEVANT PERIOD PATTERNS
    # ========================================================

    period_summary = {}


    if not similar_periods.empty:

        period_summary = {

            "average_cycle_length":
                round(
                    similar_periods[
                        "cycle_length_days"
                    ].mean(),
                    2
                ),

            "average_pain":
                round(
                    similar_periods[
                        "pain_level"
                    ].mean(),
                    2
                ),

            "average_mood":
                round(
                    similar_periods[
                        "mood_score"
                    ].mean(),
                    2
                ),

            "average_stress":
                round(
                    similar_periods[
                        "stress_score_cycle"
                    ].mean(),
                    2
                ),

            "average_sleep":
                round(
                    similar_periods[
                        "sleep_hours_cycle"
                    ].mean(),
                    2
                ),

            "average_energy":
                round(
                    similar_periods[
                        "energy_level"
                    ].mean(),
                    2
                ),

            "average_concentration":
                round(
                    similar_periods[
                        "concentration_score"
                    ].mean(),
                    2
                )
        }


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "success": True,

        "user_profile": profile,

        "latest_period": period,

        "similar_dataset_users":
            int(
                len(similar_users)
            ),

        "dataset_period_records_used":
            int(
                len(similar_periods)
            ),

        "similar_profile_patterns":
            similar_users[
                [
                    "user_id",
                    "age",
                    "bmi",
                    "diet_quality",
                    "exercise_frequency",
                    "sleep_hours",
                    "stress_score_baseline"
                ]
            ].to_dict(
                orient="records"
            ),

        "similar_period_patterns":
            period_summary
    }