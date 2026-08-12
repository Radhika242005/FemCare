import os
import pandas as pd

from backend.database import get_db_connection


# ============================================================
# DATASET
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "pcos",
    "cleaned",
    "pcos_cleaned.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_pcos_dataset():

    if not os.path.exists(DATASET_PATH):

        raise FileNotFoundError(
            f"PCOS dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    df = df.dropna(
        axis=0,
        how="all"
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


# ============================================================
# NORMALIZE COLUMN
# ============================================================

def normalize_column_name(column):

    if column is None:
        return ""

    value = str(column).strip().lower()

    for character in [
        " ",
        "_",
        "-",
        "\t",
        "\r",
        "\n"
    ]:
        value = value.replace(
            character,
            ""
        )

    return value


# ============================================================
# FIND DATASET COLUMN
# ============================================================

def find_dataset_column(
    dataframe,
    possible_names
):

    normalized_columns = {}

    for column in dataframe.columns:

        normalized_columns[
            normalize_column_name(column)
        ] = column

    for possible_name in possible_names:

        normalized_name = normalize_column_name(
            possible_name
        )

        if normalized_name in normalized_columns:

            return normalized_columns[
                normalized_name
            ]

    return None


# ============================================================
# DATASET COLUMN MAPPING
# ============================================================

def get_pcos_columns(df):

    columns = {

        "age": find_dataset_column(
            df,
            [
                "Age (yrs)",
                "Age(yrs)",
                "Age",
                "age"
            ]
        ),

        "bmi": find_dataset_column(
            df,
            [
                "BMI",
                "bmi"
            ]
        ),

        "exercise": find_dataset_column(
            df,
            [
                "Reg.Exercise(Y/N)",
                "Reg. Exercise(Y/N)",
                "RegExercise(Y/N)",
                "Regular Exercise(Y/N)",
                "Exercise(Y/N)",
                "exercise"
            ]
        ),

        "weight_gain": find_dataset_column(
            df,
            [
                "Weight gain(Y/N)",
                "Weight gain (Y/N)",
                "WeightGain(Y/N)",
                "weight_gain"
            ]
        ),

        "hair_growth": find_dataset_column(
            df,
            [
                "hairgrowth(Y/N)",
                "hair growth(Y/N)",
                "Hair growth(Y/N)",
                "Hair Growth(Y/N)",
                "HairGrowth(Y/N)",
                "hair_growth"
            ]
        ),

        "skin_darkening": find_dataset_column(
            df,
            [
                "Skin darkening (Y/N)",
                "Skin darkening(Y/N)",
                "SkinDarkening(Y/N)",
                "skin_darkening"
            ]
        ),

        "hair_loss": find_dataset_column(
            df,
            [
                "Hair loss(Y/N)",
                "Hair loss (Y/N)",
                "HairLoss(Y/N)",
                "hair_loss"
            ]
        ),

        "pimples": find_dataset_column(
            df,
            [
                "Pimples(Y/N)",
                "Pimples (Y/N)",
                "pimples"
            ]
        ),

        "fast_food": find_dataset_column(
            df,
            [
                "Fast food (Y/N)",
                "Fast food(Y/N)",
                "FastFood(Y/N)",
                "fast_food"
            ]
        ),

        "pcos": find_dataset_column(
            df,
            [
                "PCOS (Y/N)",
                "PCOS(Y/N)",
                "PCOS",
                "pcos"
            ]
        )
    }

    missing = [
        key
        for key, value in columns.items()
        if value is None
    ]

    if missing:

        raise ValueError(
            "Missing PCOS dataset columns: "
            + ", ".join(missing)
            + ". Available columns: "
            + ", ".join(
                str(column)
                for column in df.columns
            )
        )

    return columns


# ============================================================
# USER PROFILE
# ============================================================

def get_user_profile(user_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                user_id,
                age,
                bmi,
                diet_quality,
                exercise_frequency,
                sleep_hours,
                water_intake_liters,
                caffeine_intake,
                stress_score,
                birth_control_use,
                pcos_diagnosed,
                alcohol_consumption,
                smoking_status,
                stress_score_baseline,
                weight_gain,
                hair_growth,
                skin_darkening,
                hair_loss,
                pimples,
                fast_food
            FROM health_profiles
            WHERE user_id = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# BINARY
# ============================================================

def normalize_binary(value):

    if value is None:
        return None

    if isinstance(
        value,
        (int, float)
    ):

        if value == 1:
            return 1

        if value == 0:
            return 0

    value = str(
        value
    ).strip().lower()

    if value in [
        "yes",
        "y",
        "1",
        "true"
    ]:
        return 1

    if value in [
        "no",
        "n",
        "0",
        "false"
    ]:
        return 0

    return None


# ============================================================
# EXERCISE
# ============================================================

def normalize_exercise(value):

    if value is None:
        return None

    value = str(
        value
    ).strip().lower()

    if value in [
        "never",
        "none",
        "no",
        "rarely",
        "0"
    ]:
        return 0

    if value in [
        "sometimes",
        "frequently",
        "frequent",
        "regular",
        "regularly",
        "daily",
        "yes",
        "1",
        "1-2 days/week",
        "1–2 days/week",
        "1 to 2 days/week",
        "3-4 days/week",
        "3–4 days/week",
        "3 to 4 days/week",
        "5-6 days/week",
        "5–6 days/week",
        "5 to 6 days/week"
    ]:
        return 1

    return None


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value):

    if value is None:
        return None

    try:
        return float(value)

    except (
        ValueError,
        TypeError
    ):
        return None


# ============================================================
# SAFE INTEGER
# ============================================================

def safe_int(value):

    if value is None:
        return None

    try:
        return int(
            float(value)
        )

    except (
        ValueError,
        TypeError
    ):
        return None


# ============================================================
# FIND SIMILAR RECORDS
# ============================================================

def find_similar_users(
    profile,
    dataset,
    limit=5
):

    df = dataset.copy()

    columns = get_pcos_columns(
        df
    )

    # --------------------------------------------------------
    # Convert columns
    # --------------------------------------------------------

    for key in [
        "age",
        "bmi",
        "exercise",
        "weight_gain",
        "hair_growth",
        "skin_darkening",
        "hair_loss",
        "pimples",
        "fast_food",
        "pcos"
    ]:

        column = columns[key]

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=[
            columns["pcos"]
        ]
    )

    # --------------------------------------------------------
    # User values
    # --------------------------------------------------------

    user_age = safe_float(
        profile.get("age")
    )

    user_bmi = safe_float(
        profile.get("bmi")
    )

    user_exercise = normalize_exercise(
        profile.get(
            "exercise_frequency"
        )
    )

    user_values = {

        "weight_gain":
            normalize_binary(
                profile.get("weight_gain")
            ),

        "hair_growth":
            normalize_binary(
                profile.get("hair_growth")
            ),

        "skin_darkening":
            normalize_binary(
                profile.get("skin_darkening")
            ),

        "hair_loss":
            normalize_binary(
                profile.get("hair_loss")
            ),

        "pimples":
            normalize_binary(
                profile.get("pimples")
            ),

        "fast_food":
            normalize_binary(
                profile.get("fast_food")
            )
    }

    # --------------------------------------------------------
    # SCORE
    # Lower = more similar
    # --------------------------------------------------------

    df["similarity_score"] = 0.0

    # AGE
    if user_age is not None:

        df["similarity_score"] += (
            (
                df[columns["age"]]
                - user_age
            ).abs()
            / 10.0
        )

    # BMI
    if user_bmi is not None:

        df["similarity_score"] += (
            (
                df[columns["bmi"]]
                - user_bmi
            ).abs()
            / 5.0
        )

    # EXERCISE
    if user_exercise is not None:

        df["similarity_score"] += (

            (
                df[columns["exercise"]]
                != user_exercise
            )
            .astype(float)
            * 1.5

        )

    # SYMPTOMS
    for key, user_value in user_values.items():

        if user_value is None:
            continue

        column = columns[key]

        df["similarity_score"] += (

            (
                df[column]
                != user_value
            )
            .astype(float)
            * 2.0

        )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    similar = (
        df
        .sort_values(
            by="similarity_score",
            ascending=True
        )
        .head(limit)
        .copy()
    )

    return similar, columns


# ============================================================
# ANALYZE USER
# ============================================================

def analyze_pcos_user(user_id):

    # ========================================================
    # USER
    # ========================================================

    profile = get_user_profile(
        user_id
    )

    if not profile:

        return {
            "success": False,
            "message":
                "Health profile not found."
        }

    # ========================================================
    # DATASET
    # ========================================================

    dataset = load_pcos_dataset()

    # ========================================================
    # SIMILAR RECORDS
    # ========================================================

    similar, columns = find_similar_users(
        profile,
        dataset,
        limit=5
    )

    pcos_column = columns[
        "pcos"
    ]

    # ========================================================
    # OUTCOME COUNTS
    # ========================================================

    pcos_values = pd.to_numeric(
        similar[pcos_column],
        errors="coerce"
    )

    positive = int(
        (pcos_values == 1).sum()
    )

    negative = int(
        (pcos_values == 0).sum()
    )

    total = len(
        similar
    )

    if total > 0:

        percentage = round(
            (
                positive
                / total
            ) * 100,
            2
        )

    else:

        percentage = 0


    # ========================================================
    # PERSONALIZED RESULT
    # ========================================================

    if total == 0:

        screening_result = (
            "No sufficiently similar reference "
            "records were found."
        )

    elif percentage >= 80:

        screening_result = (
            "The closest reference records show "
            "a high proportion of PCOS-positive "
            "outcomes."
        )

    elif percentage >= 60:

        screening_result = (
            "The closest reference records show "
            "a higher proportion of PCOS-positive "
            "outcomes."
        )

    elif percentage >= 40:

        screening_result = (
            "The closest reference records show "
            "a mixed PCOS outcome pattern."
        )

    elif percentage > 0:

        screening_result = (
            "The closest reference records show "
            "a lower proportion of PCOS-positive "
            "outcomes, although some positive "
            "reference records were present."
        )

    else:

        screening_result = (
            "The closest reference records contain "
            "no PCOS-positive outcomes."
        )


    # ========================================================
    # SIMILAR RECORDS
    # ========================================================

    similar_records = []

    for _, row in similar.iterrows():

        bmi = safe_float(
            row[
                columns["bmi"]
            ]
        )

        similar_records.append({

            "age":
                safe_int(
                    row[
                        columns["age"]
                    ]
                ),

            "bmi":
                round(
                    bmi,
                    2
                )
                if bmi is not None
                else None,

            "exercise":
                safe_int(
                    row[
                        columns["exercise"]
                    ]
                ),

            "weight_gain":
                safe_int(
                    row[
                        columns["weight_gain"]
                    ]
                ),

            "hair_growth":
                safe_int(
                    row[
                        columns["hair_growth"]
                    ]
                ),

            "skin_darkening":
                safe_int(
                    row[
                        columns["skin_darkening"]
                    ]
                ),

            "hair_loss":
                safe_int(
                    row[
                        columns["hair_loss"]
                    ]
                ),

            "pimples":
                safe_int(
                    row[
                        columns["pimples"]
                    ]
                ),

            "fast_food":
                safe_int(
                    row[
                        columns["fast_food"]
                    ]
                ),

            "pcos_outcome":
                safe_int(
                    row[
                        columns["pcos"]
                    ]
                )
        })


    # ========================================================
    # USER PROFILE RESPONSE
    # ========================================================

    user_profile = {

        "age":
            profile.get(
                "age"
            ),

        "bmi":
            profile.get(
                "bmi"
            ),

        "diet_quality":
            profile.get(
                "diet_quality"
            ),

        "exercise_frequency":
            profile.get(
                "exercise_frequency"
            ),

        "weight_gain":
            profile.get(
                "weight_gain"
            ),

        "hair_growth":
            profile.get(
                "hair_growth"
            ),

        "skin_darkening":
            profile.get(
                "skin_darkening"
            ),

        "hair_loss":
            profile.get(
                "hair_loss"
            ),

        "pimples":
            profile.get(
                "pimples"
            ),

        "fast_food":
            profile.get(
                "fast_food"
            )
    }


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "success":
            True,

        "data_source":
            "pcos_reference_dataset",

        "dataset_records":
            len(dataset),

        "similar_records_used":
            total,

        "user_profile":
            user_profile,

        "reference_result": {

            "pcos_positive":
                positive,

            "pcos_negative":
                negative,

            "positive_percentage":
                percentage
        },

        "screening_result":
            screening_result,

        "similar_records":
            similar_records,

        "medical_notice":
            "This is a dataset-based reference analysis and is not a medical diagnosis."
    }