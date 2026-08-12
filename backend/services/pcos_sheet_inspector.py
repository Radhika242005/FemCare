import pandas as pd
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


file_path = os.path.join(
    BASE_DIR,
    "datasets",
    "pcos",
    "PCOS_data_without_infertility.xlsx"
)


print("==========================================")
print("PCOS EXCEL SHEET INSPECTION")
print("==========================================")


excel_file = pd.ExcelFile(
    file_path
)


print("\nSHEETS FOUND:")

for sheet in excel_file.sheet_names:

    print(
        "-",
        sheet
    )


print("\n")


for sheet in excel_file.sheet_names:

    print("==========================================")
    print("SHEET:", sheet)
    print("==========================================")

    df = pd.read_excel(
        file_path,
        sheet_name=sheet,
        header=None
    )

    print(
        "Rows:",
        df.shape[0]
    )

    print(
        "Columns:",
        df.shape[1]
    )

    print("\nFirst 10 rows:")

    print(
        df.head(10).to_string()
    )

    print("\n")