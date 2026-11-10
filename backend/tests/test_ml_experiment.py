import pandas as pd

from app.services.ml_experiment import run_experiment


# Classification test
classification_df = pd.DataFrame({
    "age": [22, 25, 28, 32, 35, 38, 42, 45, 48, 50,
            23, 27, 31, 36, 40, 44, 47, 51, 54, 57],
    "salary": [20000, 25000, 28000, 32000, 35000,
               38000, 42000, 45000, 48000, 50000,
               23000, 27000, 31000, 36000, 40000,
               44000, 47000, 51000, 54000, 57000],
    "city": ["Delhi", "Mumbai", "Pune", "Delhi", "Mumbai",
             "Pune", "Delhi", "Mumbai", "Pune", "Delhi",
             "Mumbai", "Pune", "Delhi", "Mumbai", "Pune",
             "Delhi", "Mumbai", "Pune", "Delhi", "Mumbai"],
    "purchased": ["No", "No", "No", "No", "No",
                  "No", "No", "No", "No", "No",
                  "Yes", "Yes", "Yes", "Yes", "Yes",
                  "Yes", "Yes", "Yes", "Yes", "Yes"]
})

classification_results = run_experiment(
    classification_df,
    target_column="purchased",
    task_type="classification"
)

print("\nCLASSIFICATION RESULTS")
print(classification_results)

# Regression test
regression_df = pd.DataFrame({
    "area": [500, 600, 700, 800, 900,
             1000, 1100, 1200, 1300, 1400,
             1500, 1600, 1700, 1800, 1900,
             2000, 2100, 2200, 2300, 2400],

    "bedrooms": [1, 1, 2, 2, 2,
                 2, 3, 3, 3, 3,
                 3, 3, 4, 4, 4,
                 4, 4, 4, 5, 5],

    "price": [20, 25, 30, 35, 40,
              45, 50, 55, 60, 65,
              70, 75, 80, 85, 90,
              95, 100, 105, 110, 115]
})

regression_results = run_experiment(
    regression_df,
    target_column="price",
    task_type="regression"
)

print("\nREGRESSION RESULTS")
print(regression_results)