import pandas as pd
from sklearn.model_selection import train_test_split

data = {
    "age": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
    "salary": [20000, 25000, 30000, 35000, 40000,
               45000, 50000, 55000, 60000, 65000],
    "purchased": ["No", "No", "No", "Yes", "Yes",
                  "Yes", "Yes", "Yes", "Yes", "Yes"]
}

df = pd.DataFrame(data)

X = df.drop(columns=["purchased"])
y = df["purchased"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining features:")
print(X_train)

print("\nTesting features:")
print(X_test)