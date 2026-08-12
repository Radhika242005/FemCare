import pandas as pd
import os


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "datasets"
)


# ============================================================
# CREATE CLEANED DIRECTORIES
# ============================================================

CLEANED_DIRS = [
    os.path.join(DATASET_DIR, "menstrual", "cleaned"),
    os.path.join(DATASET_DIR, "pregnancy", "cleaned"),
    os.path.join(DATASET_DIR, "thyroid", "cleaned")
]

for directory in CLEANED_DIRS:

    os.makedirs(
        directory,
        exist_ok=True
    )


# ============================================================
# 1. USER PROFILE
# ============================================================

user_profile_path = os.path.join(
    DATASET_DIR,
    "menstrual",
    "User_Profile.csv"
)

user_profile_output = os.path.join(
    DATASET_DIR,
    "menstrual",
    "cleaned",
    "User_Profile_cleaned.csv"
)

print("\n==========================================")
print("CLEANING USER PROFILE")
print("==========================================")


df = pd.read_csv(
    user_profile_path
)

print("Original rows:", len(df))


# Remove exact duplicate rows

df = df.drop_duplicates()


# Exercise frequency has missing values.
# Keep the missing value as "Unknown" rather than
# inventing a user's exercise behavior.

df["exercise_frequency"] = (
    df["exercise_frequency"]
    .fillna("Unknown")
)


# Save cleaned dataset

df.to_csv(
    user_profile_output,
    index=False
)

print(
    "Cleaned rows:",
    len(df)
)

print(
    "Saved:",
    user_profile_output
)


# ============================================================
# 2. PERIOD LOG
# ============================================================

period_log_path = os.path.join(
    DATASET_DIR,
    "menstrual",
    "Period_Log.csv"
)

period_log_output = os.path.join(
    DATASET_DIR,
    "menstrual",
    "cleaned",
    "Period_Log_cleaned.csv"
)

print("\n==========================================")
print("CLEANING PERIOD LOG")
print("==========================================")


period_df = pd.read_csv(
    period_log_path
)

print(
    "Original rows:",
    len(period_df)
)


# Remove exact duplicates

period_df = period_df.drop_duplicates()


# Convert date to proper date format

period_df["start_date"] = pd.to_datetime(
    period_df["start_date"],
    errors="coerce"
)


# Do NOT invent previous cycle length.
# For first cycle of a user, NULL is meaningful.

period_df.to_csv(
    period_log_output,
    index=False
)

print(
    "Cleaned rows:",
    len(period_df)
)

print(
    "Saved:",
    period_log_output
)


# ============================================================
# 3. PREGNANCY DATASET
# ============================================================

pregnancy_path = os.path.join(
    DATASET_DIR,
    "pregnancy",
    "Dataset - Updated.csv"
)

pregnancy_output = os.path.join(
    DATASET_DIR,
    "pregnancy",
    "cleaned",
    "pregnancy_cleaned.csv"
)

print("\n==========================================")
print("CLEANING PREGNANCY DATASET")
print("==========================================")


pregnancy_df = pd.read_csv(
    pregnancy_path
)

print(
    "Original rows:",
    len(pregnancy_df)
)


# Remove exact duplicate rows

pregnancy_df = pregnancy_df.drop_duplicates()


# Keep missing values as missing.
# We will handle them carefully when using
# this dataset for analysis.

pregnancy_df.to_csv(
    pregnancy_output,
    index=False
)

print(
    "Cleaned rows:",
    len(pregnancy_df)
)

print(
    "Saved:",
    pregnancy_output
)


# ============================================================
# 4. THYROID DATASET
# ============================================================

thyroid_path = os.path.join(
    DATASET_DIR,
    "thyroid",
    "thyroidDF.csv"
)

thyroid_output = os.path.join(
    DATASET_DIR,
    "thyroid",
    "cleaned",
    "thyroid_cleaned.csv"
)

print("\n==========================================")
print("CLEANING THYROID DATASET")
print("==========================================")


thyroid_df = pd.read_csv(
    thyroid_path
)

print(
    "Original rows:",
    len(thyroid_df)
)


# Remove exact duplicates

thyroid_df = thyroid_df.drop_duplicates()


# Keep missing laboratory measurements as NaN.
# We must not invent thyroid test values.

thyroid_df.to_csv(
    thyroid_output,
    index=False
)

print(
    "Cleaned rows:",
    len(thyroid_df)
)

print(
    "Saved:",
    thyroid_output
)


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("==========================================")
print("DATASET CLEANING COMPLETED")
print("==========================================")