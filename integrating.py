import pandas as pd
from pathlib import Path
import glob

prefixes = ["EDA", "HR", "BVP", "ACC", "TEMP"]

def concat_data(metric):
    # todo: use concat function in pandas
    output_file = f"{metric}.csv"

    # Initialize an empty file
    with open(output_file, "w",newline='') as outfile:
        header_written = False  # Track if the header is written

        csv_files = glob.glob(f"dmp-dataset/Resampled/resampled_{metric}_*.csv")

        if csv_files:
            for file in csv_files:
                print(f"Processing: {file}")
                try:
                    input_file = pd.read_csv(file, chunksize=50000)
                except pd.errors.EmptyDataError:
                    continue
                # Read file in chunks
                for chunk in input_file:
                    chunk.to_csv(outfile, mode="a", index=False, header=not header_written)
                    header_written = True  # Ensure header is written only once

    print(f"Merged file saved as '{output_file}'")

def integrate_data():
    for prefix in prefixes:
        concat_data(prefix)

def merge_data():

    csv_files = list(Path(".").glob("*.csv")) 

    df1 = load_and_prepare(csv_files[0])
    df2 = load_and_prepare(csv_files[1])

    merged1 = df1.merge(df2, on=["Timestamp", "Nurse ID"], how="outer")
    merged1.to_csv("merged1.csv", index=False)
    print("✅ Step 1: Merged file1.csv + file2.csv -> merged1.csv")

    df3 = load_and_prepare(csv_files[2])

    merged2 = merged1.merge(df3, on=["Timestamp", "Nurse ID"], how="outer")
    merged2.to_csv("merged2.csv", index=False)
    print("✅ Step 2: Merged merged1.csv + file3.csv -> merged2.csv")

    df4 = load_and_prepare(csv_files[3])

    merged3 = merged2.merge(df4, on=["Timestamp", "Nurse ID"], how="outer")
    merged3.to_csv("merged3.csv", index=False)
    print("✅ Step 3: Merged merged2.csv + file4.csv -> merged3.csv")

    df5 = load_and_prepare(csv_files[4])

    merged4 = merged3.merge(df5, on=["Timestamp", "Nurse ID"], how="outer")
    merged4.to_csv("final_merged.csv", index=False)
    print("✅ Step 4: Merged merged3.csv + file5.csv -> final_merged.csv")

    print("Final merged file: final_merged.csv")

def load_and_prepare(path):
    df = pd.read_csv(path).drop(columns=["datetime"], errors="ignore")
    
    # Round all float columns to 2 decimal places
    float_cols = df.select_dtypes(include=["float", "float64"]).columns
    df[float_cols] = df[float_cols].round(2)

    return df