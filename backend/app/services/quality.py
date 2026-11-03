
def check_missing_values(df):

    issues = []

    total_rows = len(df)

    if total_rows == 0:
        return issues

    missing_counts = df.isnull().sum()

    for column, count in missing_counts.items():

        if count > 0:

            percentage = round(
                (count / total_rows) * 100, 2
            )

            issues.append({
                "type": "missing_values",
                "column": column,
                "severity": "warning",
                "message": (
                    f"{column} contains {count} missing values "
                    f"({percentage}%)"
                )
            })

    return issues


def check_duplicate_rows(df):

    duplicate_count = int(df.duplicated().sum())

    issues = []

    if duplicate_count > 0:

        issues.append({
            "type": "duplicate_rows",
            "column": None,
            "severity": "warning",
            "message": (
                f"Dataset contains {duplicate_count} duplicate rows"
            )
        })

    return issues


def check_class_imbalance(df, target_column):

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found"
        )

    class_counts = df[target_column].value_counts()

    total_records = class_counts.sum()

    issues = []

    if len(class_counts) < 2 or total_records == 0:
        return issues

    class_percentages = (
        class_counts / total_records * 100
    ).round(2)

    minority_percentage = class_percentages.min()

    if minority_percentage < 20:

        issues.append({
            "type": "class_imbalance",
            "column": target_column,
            "severity": "warning",
            "message": (
                f"Target column '{target_column}' may be imbalanced. "
                f"Class distribution: "
                f"{class_percentages.to_dict()}"
            )
        })

    return issues



def check_suspicious_columns(df):

    issues = []

    identifier_keywords = (
        "id",
        "identifier",
        "uuid",
        "customer_number",
        "record_number"
    )

    for column in df.columns:

        unique_count = df[column].nunique(dropna=False)

        # Check for constant columns
        if unique_count <= 1:

            issues.append({
                "type": "constant_column",
                "column": column,
                "severity": "warning",
                "message": (
                    f"Column '{column}' contains only "
                    f"{unique_count} unique value"
                )
            })

        # Check for potential identifier columns
        elif (
            len(df) > 1
            and df[column].notna().any()
            and df[column].nunique() == df[column].notna().sum()
            and any(
                keyword in str(column).lower()
                for keyword in identifier_keywords
            )
        ):

            issues.append({
                "type": "potential_identifier",
                "column": column,
                "severity": "info",
                "message": (
                    f"Column '{column}' has unique values "
                    "and its name suggests it may be an identifier"
                )
            })

    return issues

def run_quality_checks(df, target_column=None, task_type=None):

    issues = []

    # 1. Check missing values
    issues.extend(check_missing_values(df))

    # 2. Check duplicate rows
    issues.extend(check_duplicate_rows(df))

    # 3. Check suspicious columns
    issues.extend(check_suspicious_columns(df))

    # 4. Check class imbalance only for classification
    if task_type == "classification" and target_column:
        issues.extend(
            check_class_imbalance(df, target_column)
        )

    return {
        "total_issues": len(issues),
        "issues": issues
    }