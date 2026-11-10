from sklearn.linear_model import LogisticRegression

# Training data
X_train = [
    [20],
    [25],
    [30],
    [35],
    [40],
    [45]
]

y_train = [
    "No",
    "No",
    "No",
    "Yes",
    "Yes",
    "Yes"
]

# Create model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predict for new data
predictions = model.predict([
    [22],
    [38]
])

# Get prediction probabilities
probabilities = model.predict_proba([
    [22],
    [38]
])

print("Predictions:", predictions)
print("Class labels:", model.classes_)
print("Probabilities:", probabilities)