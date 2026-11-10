import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# 1. Create dataset
data = {
    "age": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
    "salary": [20000, 25000, 30000, 35000, 40000,
               45000, 50000, 55000, 60000, 65000],
    "purchased": ["No", "No", "No", "Yes", "Yes",
                  "Yes", "Yes", "Yes", "Yes", "Yes"]
}

df = pd.DataFrame(data)


# 2. Separate features and target
X = df.drop(columns=["purchased"])
y = df["purchased"]


# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. Create model
model = LogisticRegression()


# 5. Train model
model.fit(X_train, y_train)


# 6. Predict using unseen testing data
predictions = model.predict(X_test)


# 7. Evaluate model
accuracy = accuracy_score(y_test, predictions)

print("Actual values:")
print(y_test.tolist())

print("\nPredicted values:")
print(predictions.tolist())

print("\nAccuracy:", accuracy)