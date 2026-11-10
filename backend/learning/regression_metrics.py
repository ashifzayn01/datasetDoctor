# from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# actual = [50, 60, 70]
# predicted = [48, 65, 68]

# mae = mean_absolute_error(actual, predicted)
# rmse = root_mean_squared_error(actual, predicted)

# print("MAE:", mae)
# print("RMSE:", rmse)


# import pandas as pd
# from sklearn.impute import SimpleImputer

# data = {
#     "age": [25, 30, None, 40],
#     "salary": [20000, None, 35000, 40000]
# }

# df = pd.DataFrame(data)

# imputer = SimpleImputer(strategy="median")

# transformed_data = imputer.fit_transform(df)

# result = pd.DataFrame(
#     transformed_data,
#     columns=df.columns
# )

# print("Original dataset:")
# print(df)

# print("\nAfter imputation:")
# print(result)


# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder

# data = {
#     "city": ["Delhi", "Mumbai", "Pune", "Delhi"]
# }

# df = pd.DataFrame(data)

# encoder = OneHotEncoder(
#     sparse_output=False,
#     handle_unknown="ignore"
# )

# encoded_data = encoder.fit_transform(df[["city"]])

# encoded_df = pd.DataFrame(
#     encoded_data,
#     columns=encoder.get_feature_names_out(["city"])
# )

# print("Original data:")
# print(df)

# print("\nEncoded data:")
# print(encoded_df)

# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# data = {
#     "age": [20, 30, 40],
#     "salary": [20000, 40000, 60000]
# }

# df = pd.DataFrame(data)

# scaler = StandardScaler()

# scaled_data = scaler.fit_transform(df)

# scaled_df = pd.DataFrame(
#     scaled_data,
#     columns=df.columns
# )

# print("Original data:")
# print(df)

# print("\nScaled data:")
# print(scaled_df)

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

data = {
    "age": [25, 30, None, 40],
    "salary": [20000, None, 35000, 40000],
    "city": ["Delhi", "Mumbai", "Pune", "Delhi"]
}

df = pd.DataFrame(data)

numeric_features = ["age", "salary"]
categorical_features = ["city"]

# Numerical preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical preprocessing
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Combine both preprocessing pipelines
preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

# Apply preprocessing
transformed_data = preprocessor.fit_transform(df)

print("Original dataset:")
print(df)

print("\nTransformed dataset:")
print(transformed_data)

print("\nOutput shape:")
print(transformed_data.shape)