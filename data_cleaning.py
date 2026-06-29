"""
Data Analyst Internship - Task 1: Data Cleaning and Preprocessing
Dataset: Customer Purchase Data (custom raw dataset)
Tools: Python (Pandas)
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# STEP 1: Load the raw dataset
# ─────────────────────────────────────────────
print("=" * 55)
print("STEP 1: Loading Raw Dataset")
print("=" * 55)

df = pd.read_csv("raw_dataset.csv", dtype={"Phone": str})

print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print("\nFirst 5 rows:")
print(df.head())
print("\nData Types:")
print(df.dtypes)


# ─────────────────────────────────────────────
# STEP 2: Initial Data Quality Check
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 2: Initial Data Quality Check")
print("=" * 55)

print("\nMissing Values per Column:")
print(df.isnull().sum())
print(f"\nDuplicate Rows Found: {df.duplicated().sum()}")
print("\nUnique Gender Values (before):", df["Gender"].unique())
print("Unique Country Values (before):", df["Country"].unique())


# ─────────────────────────────────────────────
# STEP 3: Remove Duplicate Rows
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 3: Removing Duplicate Rows")
print("=" * 55)

before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]
print(f"Rows before: {before} | After: {after} | Removed: {before - after}")


# ─────────────────────────────────────────────
# STEP 4: Rename Columns (lowercase, underscores)
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 4: Renaming Column Headers")
print("=" * 55)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Columns:", list(df.columns))


# ─────────────────────────────────────────────
# STEP 5: Handle Missing Values
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 5: Handling Missing Values")
print("=" * 55)

# Name
n = df["name"].isnull().sum()
df["name"] = df["name"].fillna("Unknown")
print(f"'name'   -> {n} missing filled with 'Unknown'")

# Age (median)
n = df["age"].isnull().sum()
median_age = int(df["age"].median())
df["age"] = df["age"].fillna(median_age)
print(f"'age'    -> {n} missing filled with median ({median_age})")

# Gender (replace invalid chars first)
df["gender"] = df["gender"].replace(["-", "", " "], np.nan)
n = df["gender"].isnull().sum()
df["gender"] = df["gender"].fillna("Unknown")
print(f"'gender' -> {n} missing/invalid filled with 'Unknown'")

# Country
n = df["country"].isnull().sum()
df["country"] = df["country"].fillna("Unknown")
print(f"'country'-> {n} missing filled with 'Unknown'")

# Phone (already read as string)
n = df["phone"].isnull().sum()
df["phone"] = df["phone"].fillna("Not Provided")
print(f"'phone'  -> {n} missing filled with 'Not Provided'")


# ─────────────────────────────────────────────
# STEP 6: Standardize Text Values
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 6: Standardizing Text Values")
print("=" * 55)

gender_map = {
    "male": "Male",   "m": "Male",
    "female": "Female", "f": "Female",
    "unknown": "Unknown"
}
df["gender"] = df["gender"].str.strip().str.lower().map(gender_map).fillna("Unknown")
print("Gender unique values after :", df["gender"].unique())

df["country"] = df["country"].str.strip().str.title()
print("Country unique values after:", df["country"].unique())

df["name"] = df["name"].str.strip().str.title()


# ─────────────────────────────────────────────
# STEP 7: Fix Date Format -> dd-mm-yyyy
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 7: Standardizing Date Format")
print("=" * 55)

print("Sample dates before:", df["date_of_purchase"].head(4).tolist())
df["date_of_purchase"] = pd.to_datetime(
    df["date_of_purchase"], dayfirst=False, format="mixed"
)
df["date_of_purchase"] = df["date_of_purchase"].dt.strftime("%d-%m-%Y")
print("Sample dates after :", df["date_of_purchase"].head(4).tolist())


# ─────────────────────────────────────────────
# STEP 8: Fix Data Types
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 8: Fixing Data Types")
print("=" * 55)

df["age"] = df["age"].astype(int)
df["purchase_amount"] = df["purchase_amount"].astype(float)
df["customerid"] = df["customerid"].astype(int)

print("Final Data Types:")
print(df.dtypes)


# ─────────────────────────────────────────────
# STEP 9: Outlier Check (IQR Method)
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 9: Outlier Check on purchase_amount (IQR)")
print("=" * 55)

Q1 = df["purchase_amount"].quantile(0.25)
Q3 = df["purchase_amount"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df["purchase_amount"] < lower) | (df["purchase_amount"] > upper)]
print(f"IQR bounds: [{lower:.2f}, {upper:.2f}]")
print(f"Outliers found: {len(outliers)}")
if not outliers.empty:
    print(outliers[["name", "purchase_amount"]])
else:
    print("No outliers detected.")


# ─────────────────────────────────────────────
# STEP 10: Save Cleaned Dataset
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("STEP 10: Saving Cleaned Dataset")
print("=" * 55)

df.reset_index(drop=True, inplace=True)
df.to_csv("cleaned_dataset.csv", index=False)

print(f"Final shape: {df.shape[0]} rows x {df.shape[1]} columns")
print("\nCleaned Dataset:")
print(df.to_string(index=False))
print("\n[OK] cleaned_dataset.csv saved successfully!")


# ─────────────────────────────────────────────
# CLEANING SUMMARY
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("CLEANING SUMMARY REPORT")
print("=" * 55)
print("""
Step | Action                         | Details
-----|--------------------------------|--------------------------------------
  1  | Loaded raw data                | 25 rows x 9 columns
  2  | Data quality audit             | Nulls, duplicates & format issues found
  3  | Removed duplicate rows         | 2 duplicate rows dropped (23 remain)
  4  | Renamed column headers         | Lowercase + underscores (no spaces)
  5  | Filled missing values          | age->median, others->'Unknown'
  6  | Standardized gender & country  | M/F/FEMALE/male -> Male/Female
  7  | Unified date format            | Mixed formats -> dd-mm-yyyy
  8  | Fixed data types               | age->int, purchase_amount->float
  9  | Outlier check (IQR method)     | No outliers in purchase_amount
 10  | Saved cleaned_dataset.csv      | Ready for analysis/modelling
""")
