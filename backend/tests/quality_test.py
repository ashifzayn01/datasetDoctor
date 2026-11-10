import pandas as pd

from app.services.quality import (
    check_missing_values,
    check_duplicate_rows,
    check_class_imbalance,
    check_suspicious_columns,
    run_quality_checks
)


# Test 1: Missing values and duplicate rows

data = {
    "name": ["Ashif", "Rahul", "Ashif", "Aman"],
    "age": [22, 24, 22, None],
    "salary": [25000, 30000, 25000, 28000]
}

df = pd.DataFrame(data)

print("\n========== TEST 1 ==========")

print("Missing Value Issues:")
print(check_missing_values(df))

print("\nDuplicate Row Issues:")
print(check_duplicate_rows(df))


# Test 2: Class imbalance

data = {
    "age": [22, 24, 25, 23, 26, 28, 29, 30, 31, 32],
    "purchased": [
        "Yes", "Yes", "Yes", "Yes", "No",
        "Yes", "Yes", "Yes", "Yes", "Yes"
    ]
}

df = pd.DataFrame(data)

print("\n========== TEST 2 ==========")

print("Class Imbalance Issues:")
print(check_class_imbalance(df, "purchased"))


# Test 3: Suspicious columns

data = {
    "customer_id": ["C001", "C002", "C003", "C004"],
    "age": [22, 24, 25, 23],
    "salary": [25000, 30000, 28000, 35000],
    "country": ["India", "India", "India", "India"]
}

df = pd.DataFrame(data)

print("\n========== TEST 3 ==========")

print("Suspicious Column Issues:")
print(check_suspicious_columns(df))


# Test 4: Invalid target column

print("\n========== TEST 4 ==========")

try:
    print(check_class_imbalance(df, "invalid_column"))

except ValueError as error:
    print("Expected Error:", error)


# Test 5: Combined quality checks - Classification

print("\n========== TEST 5 ==========")

data = {
    "customer_id": ["C001", "C002", "C003", "C004", "C005"],
    "age": [22, 24, 25, 23, 26],
    "purchased": ["Yes", "Yes", "Yes", "Yes", "No"]
}

df = pd.DataFrame(data)

result = run_quality_checks(
    df,
    target_column="purchased",
    task_type="classification"
)

print(result)


# Test 6: Combined quality checks - Regression

print("\n========== TEST 6 ==========")

data = {
    "age": [22, 24, 25, 23, 26],
    "salary": [25000, 30000, 28000, 35000, 32000]
}

df = pd.DataFrame(data)

result = run_quality_checks(
    df,
    target_column="salary",
    task_type="regression"
)

print(result)