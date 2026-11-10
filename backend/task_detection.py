import pandas as pd

def detect_task_type(series):

    series = series.dropna()

    if series.empty:
        raise ValueError("Target column contains no valid values")

    dtype = series.dtype

    # Text, Boolean and categorical targets
    if (
        pd.api.types.is_bool_dtype(dtype)
        or isinstance(dtype, pd.CategoricalDtype)
        or pd.api.types.is_object_dtype(dtype)
        or isinstance(dtype, pd.StringDtype)
    ):
        return "classification"

    # Numeric targets
    if pd.api.types.is_numeric_dtype(dtype):

        unique_count = series.nunique()

        # Binary numeric target, e.g. 0 and 1
        if unique_count == 2:
            return "classification"

        unique_ratio = unique_count / len(series)

        # Low-cardinality integer target
        if (
            pd.api.types.is_integer_dtype(dtype)
            and unique_count <= 10
            and unique_ratio <= 0.05
        ):
            return "classification"

        return "regression"

    raise ValueError("Unsupported target data type")