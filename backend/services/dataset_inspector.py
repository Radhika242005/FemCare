import pandas as pd
import os


# ============================================================
# PROJECT DATASET PATH
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
# DATASET INSPECTION FUNCTION
# ============================================================

def inspect_dataset(name, file_path, file_type="csv", sheet_name=None):

    print("\n")
    print("=" * 70)
    print(f"DATASET: {name}")
    print("=" * 70)

    print(f"File: {file_path}")

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.exists(file_path):

        print("ERROR: File not found.")

        return

    try:

        # ----------------------------------------------------
        # Read CSV
        # ----------------------------------------------------

        if file_type == "csv":

            df = pd.read_csv(file_path)

        # ----------------------------------------------------
        # Read Excel
        # ----------------------------------------------------

        elif file_type == "excel":

            if sheet_name:

                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name
                )

            else:

                df = pd.read_excel(file_path)

        else:

            print("Unsupported file type.")

            return


        # ----------------------------------------------------
        # Basic information
        # ----------------------------------------------------

        print("\nROWS:")
        print(df.shape[0])

        print("\nCOLUMNS:")
        print(df.shape[1])


        # ----------------------------------------------------
        # Column names
        # ----------------------------------------------------

        print("\nCOLUMN NAMES:")

        for index, column in enumerate(df.columns):

            print(
                f"{index + 1}. {column}"
            )


        # ----------------------------------------------------
        # Data types
        # ----------------------------------------------------

        print("\nDATA TYPES:")

        print(df.dtypes)


        # ----------------------------------------------------
        # Missing values
        # ----------------------------------------------------

        print("\nMISSING VALUES:")

        missing_values = df.isnull().sum()

        print(missing_values)


        # ----------------------------------------------------
        # Duplicate rows
        # ----------------------------------------------------

        duplicate_count = df.duplicated().sum()

        print("\nDUPLICATE ROWS:")

        print(duplicate_count)


        # ----------------------------------------------------
        # First 5 rows
        # ----------------------------------------------------

        print("\nFIRST 5 ROWS:")

        print(
            df.head().to_string()
        )


        # ----------------------------------------------------
        # Numeric summary
        # ----------------------------------------------------

        print("\nNUMERIC SUMMARY:")

        print(
            df.describe(
                include="number"
            ).to_string()
        )


        print("\nINSPECTION COMPLETED.")


    except Exception as error:

        print("\nERROR WHILE READING DATASET:")

        print(error)


# ============================================================
# DATASET PATHS
# ============================================================

menstrual_period = os.path.join(
    DATASET_DIR,
    "menstrual",
    "Period_Log.csv"
)


menstrual_profile = os.path.join(
    DATASET_DIR,
    "menstrual",
    "User_Profile.csv"
)


pcos_dataset = os.path.join(
    DATASET_DIR,
    "pcos",
    "PCOS_data_without_infertility.xlsx"
)


pregnancy_dataset = os.path.join(
    DATASET_DIR,
    "pregnancy",
    "Dataset - Updated.csv"
)


thyroid_dataset = os.path.join(
    DATASET_DIR,
    "thyroid",
    "thyroidDF.csv"
)


# ============================================================
# RUN INSPECTIONS
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("#" * 70)
    print("                 FEMCARE DATASET INSPECTION")
    print("#" * 70)


    # --------------------------------------------------------
    # Menstrual Profile
    # --------------------------------------------------------

    inspect_dataset(
        "Menstrual - User Profile",
        menstrual_profile
    )


    # --------------------------------------------------------
    # Menstrual Period Log
    # --------------------------------------------------------

    inspect_dataset(
        "Menstrual - Period Log",
        menstrual_period
    )


    # --------------------------------------------------------
    # PCOS
    # --------------------------------------------------------

    inspect_dataset(
        "PCOS",
        pcos_dataset,
        file_type="excel"
    )


    # --------------------------------------------------------
    # Pregnancy
    # --------------------------------------------------------

    inspect_dataset(
        "Pregnancy",
        pregnancy_dataset
    )


    # --------------------------------------------------------
    # Thyroid
    # --------------------------------------------------------

    inspect_dataset(
        "Thyroid",
        thyroid_dataset
    )


    print("\n")
    print("#" * 70)
    print("              ALL DATASETS INSPECTED")
    print("#" * 70)