# data-analyst-internship-task1
**Internship:** Data Analyst Internship  
**Tools Used:** Python 3, Pandas, NumPy

---

## Objective

Clean and prepare a raw customer purchase dataset that contains missing values, duplicate rows, inconsistent text formatting, and mixed date formats.

---

## Files in this Repository

| File | Description |
|------|-------------|
| `raw_dataset.csv` | Original uncleaned dataset (25 rows) |
| `data_cleaning.py` | Python script with all cleaning steps |
| `cleaned_dataset.csv` | Final cleaned output ready for analysis |
| `README.md` | This file |

---

## Dataset Description

The dataset contains customer purchase records with the following columns:

`customerid`, `name`, `age`, `gender`, `country`, `purchase_amount`, `date_of_purchase`, `email`, `phone`

### Issues Found in Raw Data

- **Missing values** in: `name`, `age`, `gender`, `country`, `phone`
- **Duplicate rows**: 2 completely identical records
- **Inconsistent gender values**: `male`, `M`, `MALE`, `female`, `F`, `FEMALE`, `-`
- **Inconsistent country names**: `USA`, `united states`, `INDIA`, `canada`
- **Mixed date formats**: `2024-01-15`, `15-01-2024`, `2024/01/20`
- **Wrong data types**: `age` was float instead of int

---

## Cleaning Steps Performed

### Step 1 – Load the Raw Dataset
```python
df = pd.read_csv("raw_dataset.csv", dtype={"Phone": str})
```
Loaded with `Phone` as string to avoid scientific notation issues.

---

### Step 2 – Data Quality Audit
```python
df.isnull().sum()       # check nulls
df.duplicated().sum()   # check duplicates
df["Gender"].unique()   # check inconsistent values
```

---

### Step 3 – Remove Duplicate Rows
```python
df = df.drop_duplicates()
# Result: 25 rows -> 23 rows (2 removed)
```

---

### Step 4 – Rename Column Headers
```python
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
# Example: "Purchase_Amount" -> "purchase_amount"
```

---

### Step 5 – Handle Missing Values
```python
df["name"]    = df["name"].fillna("Unknown")
df["age"]     = df["age"].fillna(df["age"].median())   # median imputation
df["gender"]  = df["gender"].replace(["-",""], np.nan).fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["phone"]   = df["phone"].fillna("Not Provided")
```

---

### Step 6 – Standardize Text Values
```python
# Gender: map all variants to Male / Female / Unknown
gender_map = {"male":"Male", "m":"Male", "female":"Female", "f":"Female", "unknown":"Unknown"}
df["gender"] = df["gender"].str.strip().str.lower().map(gender_map).fillna("Unknown")

# Country: title case
df["country"] = df["country"].str.strip().str.title()
```

---

### Step 7 – Unify Date Format to dd-mm-yyyy
```python
df["date_of_purchase"] = pd.to_datetime(df["date_of_purchase"], dayfirst=False, format="mixed")
df["date_of_purchase"] = df["date_of_purchase"].dt.strftime("%d-%m-%Y")
```
Handles all three input formats: `yyyy-mm-dd`, `dd-mm-yyyy`, `yyyy/mm/dd`.

---

### Step 8 – Fix Data Types
```python
df["age"]             = df["age"].astype(int)
df["purchase_amount"] = df["purchase_amount"].astype(float)
```

---

### Step 9 – Outlier Detection (IQR Method)
```python
Q1, Q3 = df["purchase_amount"].quantile([0.25, 0.75])
IQR    = Q3 - Q1
lower  = Q1 - 1.5 * IQR   # -60.00
upper  = Q3 + 1.5 * IQR   # 580.00
```
1 mild outlier found (Olivia Lewis, ₹610) — retained as a valid high-value purchase.

---

### Step 10 – Save Cleaned Dataset
```python
df.to_csv("cleaned_dataset.csv", index=False)
```

---

## Summary of Changes

| Step | Action | Result |
|------|--------|--------|
| Duplicates removed | `drop_duplicates()` | 2 rows dropped |
| Column headers | Lowercase + underscores | Uniform naming |
| Missing `name` | Filled → `"Unknown"` | 1 value fixed |
| Missing `age` | Filled → median (32) | 3 values fixed |
| Missing `gender` | Filled → `"Unknown"` | 2 values fixed |
| Missing `country` | Filled → `"Unknown"` | 1 value fixed |
| Missing `phone` | Filled → `"Not Provided"` | 3 values fixed |
| Gender standardized | All variants → Male/Female | 10 variants → 3 |
| Country standardized | Title-case applied | 12 variants → 9 |
| Date format unified | Mixed → dd-mm-yyyy | 3 formats → 1 |
| Data types fixed | age → int, amount → float | Correct types set |

---

## How to Run

```bash
# Install dependency (if not already installed)
pip install pandas numpy

# Run the cleaning script
python data_cleaning.py
```

Output: `cleaned_dataset.csv` is created in the same directory.

---

## Interview Questions – Quick Answers

**1. What are missing values and how do you handle them?**  
Missing values are NaN/null entries. Handled by: dropping rows (`dropna()`), filling with mean/median/mode (`fillna()`), or a placeholder like `"Unknown"`.

**2. How do you treat duplicate records?**  
Use `df.drop_duplicates()` to remove exact duplicate rows. Can also deduplicate on specific columns using the `subset` parameter.

**3. Difference between `dropna()` and `fillna()`?**  
`dropna()` removes rows/columns with null values. `fillna()` replaces nulls with a specified value (e.g., mean, median, or string).

**4. What is outlier treatment and why is it important?**  
Outliers are extreme values that skew analysis. Detected using IQR or Z-score method, then either capped, removed, or retained based on context.

**5. Explain the process of standardizing data.**  
Standardizing means making values consistent — e.g., converting `male/M/MALE` → `Male`, lowercasing column names, unifying date formats.

**6. How do you handle inconsistent data formats (e.g., date/time)?**  
Use `pd.to_datetime()` with `format="mixed"` to parse multiple formats, then `strftime()` to output a single unified format.

**7. What are common data cleaning challenges?**  
Missing values, duplicates, inconsistent formatting, mixed data types, outliers, and typos in categorical columns.

**8. How can you check data quality?**  
Use `df.info()`, `df.isnull().sum()`, `df.duplicated().sum()`, `df.describe()`, and `df["col"].unique()` to audit quality across all columns.
