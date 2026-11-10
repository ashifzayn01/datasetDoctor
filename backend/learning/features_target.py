import pandas as pd

# Sample dataset
data = {
    "customer_id": ["C001", "C002", "C003", "C004"],
    "age": [22, 24, 28, 23],
    "salary": [25000, 30000, 28000, 35000],
    "purchased": ["Yes", "No", "Yes", "Yes"]
}

df = pd.DataFrame(data)

# Select target column
target_column = "purchased"

# Create X (features)
X = df.drop(columns=[target_column, "customer_id"])

# Create y (target)
y = df[target_column]

print("Features (X):")
print(X)

print("\nTarget (y):")
print(y)