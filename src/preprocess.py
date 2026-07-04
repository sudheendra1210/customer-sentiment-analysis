import pandas as pd


def clean_data(df):

    print("\n========== DATA CLEANING ==========\n")

    # Dataset shape before cleaning
    print(f"Original Shape : {df.shape}")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    print(f"Duplicate Rows : {duplicates}")

    df = df.drop_duplicates()

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Remove rows with missing values
    df = df.dropna()

    # Remove extra spaces
    df["Review"] = df["Review"].astype(str).str.strip()
    df["Sentiment"] = df["Sentiment"].astype(str).str.strip()

    print(f"\nFinal Shape : {df.shape}")

    print("\n✅ Data Cleaning Completed Successfully!\n")

    return df