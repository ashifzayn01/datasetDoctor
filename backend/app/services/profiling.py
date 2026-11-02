
def profile_dataset(df):

    if not df.columns.is_unique:
        duplicate_columns = df.columns[
            df.columns.duplicated()
        ].tolist()

        raise ValueError(
            f"Duplicate column names found: {duplicate_columns}"
        )


    # 1. Missing values
    missing_values = df.isnull().sum().to_dict()

    # 2. Missing-value percentages
    if len(df) == 0:
        missing_percentage = {
            column: None for column in df.columns
        }
    else:
        missing_percentage = (
            df.isnull().sum() / len(df) * 100
        ).round(2).to_dict()

    # 3. Duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # 4. Column data types
    column_types = df.dtypes.astype(str).to_dict()

    # 5. Unique values
    unique_values = df.nunique().to_dict()

    # 6. Numerical statistics
    numeric_columns = df.select_dtypes(include=["number"]).columns
    if len(numeric_columns) == 0:
        numeric_stats = {}
    else:
        numeric_stats = df[numeric_columns].describe().to_dict()
    
   

    # 7. Categorical statistics
    categorical_columns = df.select_dtypes(
        include=["object", "str", "category"]
    ).columns

    categorical_stats = {}

    for column in categorical_columns:
        value_counts = df[column].value_counts()

        categorical_stats[column] = {
            "unique_values": int(df[column].nunique()),
            "most_frequent": value_counts.index[0] if not value_counts.empty else None,
            "most_frequent_count": int(value_counts.iloc[0]) if not value_counts.empty else 0
        }

    # 8. Final profile
    profile = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
        "duplicate_rows": duplicate_rows,
        "column_types": column_types,
        "unique_values": unique_values,
        "numeric_statistics": numeric_stats,
        "categorical_statistics": categorical_stats
    }

    return profile
