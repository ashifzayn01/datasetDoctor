import pandas as pd
from app.services.ml_experiment import run_experiment


df = pd.DataFrame({
    "age": range(10),
    "city": ["Delhi", "Mumbai"] * 5,
    "purchased": ["Yes", "No"] * 5,
    "price": range(100, 110)
})


def expect_error(test_name, test_function):

    try:
        test_function()
        print(f"FAILED: {test_name} — no error raised")

    except ValueError as error:
        print(f"PASSED: {test_name} — {error}")


# 1. Target column does not exist
expect_error(
    "Missing target column",
    lambda: run_experiment(df, "salary", "classification")
)

# 2. Unsupported task type
expect_error(
    "Invalid task type",
    lambda: run_experiment(df, "purchased", "clustering")
)

# 3. Target contains only one class
single_class_df = df.copy()
single_class_df["purchased"] = ["Yes"] * 10

expect_error(
    "Single-class target",
    lambda: run_experiment(single_class_df, "purchased", "classification")
)

# 4. Insufficient valid target records
missing_target_df = df.copy()
missing_target_df.loc[:2, "purchased"] = None

expect_error(
    "Insufficient valid records",
    lambda: run_experiment(missing_target_df, "purchased", "classification")
)

# 5. No feature columns
target_only_df = pd.DataFrame({
    "purchased": ["Yes", "No"] * 5
})

expect_error(
    "No feature columns",
    lambda: run_experiment(target_only_df, "purchased", "classification")
)

# 6. Non-numeric regression target
invalid_regression_df = df.copy()
invalid_regression_df["price"] = ["high", "low"] * 5

expect_error(
    "Invalid regression target",
    lambda: run_experiment(invalid_regression_df, "price", "regression")
)