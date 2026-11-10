
import pandas as pd

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    root_mean_squared_error
)


def build_preprocessor(X, scale_numeric=True):

    numeric_columns = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    transformers = []

    if numeric_columns:
        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ])

        if scale_numeric:
            numeric_pipeline.steps.append(
                ("scaler", StandardScaler())
            )

        transformers.append(
            ("numeric", numeric_pipeline, numeric_columns)
        )

    if categorical_columns:
        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ])

        transformers.append(
            ("categorical", categorical_pipeline, categorical_columns)
        )

    if not transformers:
        raise ValueError("No usable feature columns found.")

    return ColumnTransformer(transformers)


def get_models(task_type):

    if task_type == "classification":
        return {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        }

    elif task_type == "regression":
        return {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
        }

    raise ValueError("Unsupported task type.")


def run_experiment(df, target_column, task_type):

    # 1. Basic validation
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("Dataset is empty.")

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' does not exist."
        )

    if task_type not in ["classification", "regression"]:
        raise ValueError(
            "Task type must be classification or regression."
        )

    # 2. Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # 3. Remove rows with missing target values
    valid_rows = y.notna()
    X = X.loc[valid_rows].copy()
    y = y.loc[valid_rows].copy()

    if len(X) < 10:
        raise ValueError(
            "At least 10 records with valid target values are required."
        )

    if X.shape[1] == 0:
        raise ValueError("No feature columns available.")

    if y.nunique() < 2:
        raise ValueError(
            "Target column must contain at least 2 unique values."
        )

    # 4. Validate target type
    if task_type == "classification":

        if y.dtype == "object":
            y = y.astype(str)

        class_counts = y.value_counts()

        if class_counts.min() < 2:
            raise ValueError(
                "Each class needs at least 2 records for stratified splitting."
            )

    else:

        y = pd.to_numeric(y, errors="coerce")

        if y.isna().any():
            raise ValueError(
                "Regression target must contain only numerical values."
            )

        if not y.map(
            lambda value: pd.notna(value)
            and abs(value) != float("inf")
        ).all():
            raise ValueError(
                "Regression target contains infinite values."
            )

    # 5. Validate feature columns
    X = X.replace(
        [float("inf"), float("-inf")],
        float("nan")
    )

    # Remove completely empty feature columns
    X = X.dropna(axis=1, how="all")

    if X.shape[1] == 0:
        raise ValueError(
            "All feature columns are empty or unusable."
        )

    # 6. Split dataset
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y if task_type == "classification" else None
        )

    except ValueError as error:
        raise ValueError(
            f"Unable to split dataset into training and testing sets: {error}"
        )

    # 7. Get candidate models
    models = get_models(task_type)

    results = []

    # 8. Train and evaluate models
    for model_name, model in models.items():

        scale_numeric = (
            model_name in ["Logistic Regression", "Linear Regression"]
        )

        preprocessor = build_preprocessor(
            X_train,
            scale_numeric=scale_numeric
        )

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        # 9. Calculate evaluation metrics
        if task_type == "classification":

            metrics = {
                "accuracy": float(
                    accuracy_score(y_test, predictions)
                ),
                "precision": float(
                    precision_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                ),
                "recall": float(
                    recall_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                ),
                "f1_score": float(
                    f1_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                    )
                )
            }

        else:

            metrics = {
                "mae": float(
                    mean_absolute_error(y_test, predictions)
                ),
                "rmse": float(
                    root_mean_squared_error(y_test, predictions)
                )
            }

        results.append({
            "model_name": model_name,
            "metrics": metrics
        })

    # 10. Return experiment results
    return {
        "task_type": task_type,
        "target_column": target_column,
        "total_records": len(X),
        "train_records": len(X_train),
        "test_records": len(X_test),
        "feature_columns": X.columns.tolist(),
        "model_results": results
    }
