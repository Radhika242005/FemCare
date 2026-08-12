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

INPUT_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "pcos",
    "PCOS_data_without_infertility.xlsx"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "datasets",
    "pcos",
    "cleaned"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "pcos_cleaned.csv"
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


print("==========================================")
print("PCOS DATASET CLEANING")
print("==========================================")


# ============================================================
# READ ACTUAL DATA SHEET
# ============================================================

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="Full_new"
)


print("Original rows:", len(df))
print("Original columns:", len(df.columns))


# ============================================================
# REMOVE COMPLETELY EMPTY COLUMNS
# ============================================================

df = df.dropna(
    axis=1,
    how="all"
)


# ============================================================
# REMOVE COMPLETELY EMPTY ROWS
# ============================================================

df = df.dropna(
    axis=0,
    how="all"
)


# ============================================================
# REMOVE DUPLICATE ROWS
# ============================================================

df = df.drop_duplicates()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = [
    str(column).strip()
    for column in df.columns
]

# ============================================================
# REMOVE UNNECESSARY EXCEL COLUMNS
# ============================================================

df = df.loc[
    :,
    ~df.columns.str.startswith("Unnamed:")
]
# ============================================================
# SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("Cleaned rows:", len(df))
print("Cleaned columns:", len(df.columns))

print("\nColumns:")

for column in df.columns:

    print(
        "-",
        column
    )


print("\nSaved:")
print(OUTPUT_FILE)


print("\n==========================================")
print("PCOS CLEANING COMPLETED")
print("==========================================")