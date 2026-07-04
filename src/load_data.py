import pandas as pd
from preprocess import clean_data


def load_dataset():

    df = pd.read_csv("data/flipkart.csv")

    print("✅ Dataset Loaded Successfully!")

    df = clean_data(df)

    print("\nFirst 5 Rows:\n")
    print(df.head())

    return df


if __name__ == "__main__":
    load_dataset()