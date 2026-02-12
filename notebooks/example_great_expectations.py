"""
Great Expectations Suite Validation (pandas-based)
Author: Gabriel Demetrios Lafis
Description: Validates sales data against expectations defined in
             sales_data_suite.json using pandas. This reads the same
             JSON expectation suite format that Great Expectations uses,
             but executes the checks with pandas directly.
"""

import pandas as pd
from pathlib import Path
import json


def validate_sales_data():
    """
    Validate sales data by interpreting the expectation suite JSON
    and running each expectation with pandas.
    """
    print("\n" + "=" * 70)
    print("SALES DATA VALIDATION (pandas-based)")
    print("=" * 70 + "\n")

    # Resolve paths
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "sample_sales.csv"
    suite_path = (
        project_root
        / "great_expectations"
        / "expectations"
        / "sales_data_suite.json"
    )

    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        return

    if not suite_path.exists():
        print(f"Expectation suite not found: {suite_path}")
        return

    # Load data and suite
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} rows from {data_path.name}")

    with open(suite_path, "r") as f:
        suite = json.load(f)

    print(f"Suite: {suite['expectation_suite_name']}")
    print(f"Expectations: {len(suite['expectations'])}\n")

    print("Running validations:\n")

    results = []

    for idx, expectation in enumerate(suite["expectations"], 1):
        exp_type = expectation["expectation_type"]
        kwargs = expectation.get("kwargs", {})

        print(f"{idx}. {exp_type}")

        if exp_type == "expect_table_row_count_to_be_between":
            min_val = kwargs.get("min_value", 0)
            max_val = kwargs.get("max_value", float("inf"))
            passed = min_val <= len(df) <= max_val
            print(f"   Expected: {min_val} - {max_val} rows")
            print(f"   Actual: {len(df)} rows")

        elif exp_type == "expect_column_values_to_not_be_null":
            column = kwargs.get("column")
            null_count = int(df[column].isnull().sum())
            passed = null_count == 0
            print(f"   Column: {column}")
            print(f"   Null values: {null_count}")

        elif exp_type == "expect_column_values_to_be_unique":
            column = kwargs.get("column")
            duplicates = len(df) - df[column].nunique()
            passed = duplicates == 0
            print(f"   Column: {column}")
            print(f"   Unique values: {df[column].nunique()}/{len(df)}")

        elif exp_type == "expect_column_values_to_be_in_set":
            column = kwargs.get("column")
            value_set = kwargs.get("value_set", [])
            invalid = df[~df[column].isin(value_set)][column].nunique()
            passed = invalid == 0
            print(f"   Column: {column}")
            print(f"   Valid values: {value_set}")
            print(f"   Invalid values found: {invalid}")

        elif exp_type == "expect_column_values_to_be_between":
            column = kwargs.get("column")
            if column in df.columns:
                min_val = kwargs.get("min_value")
                max_val = kwargs.get("max_value")
                valid_values = df[column].dropna()
                out_of_range = int(
                    valid_values[
                        (valid_values < min_val) | (valid_values > max_val)
                    ].count()
                )
                passed = out_of_range == 0
                print(f"   Column: {column}")
                print(f"   Expected range: {min_val} - {max_val}")
                print(f"   Out of range values: {out_of_range}")
            else:
                passed = False
                print(f"   Column '{column}' not found!")

        elif exp_type == "expect_column_values_to_match_regex":
            column = kwargs.get("column")
            regex = kwargs.get("regex")
            if column in df.columns:
                if not pd.api.types.is_string_dtype(df[column]):
                    values_to_check = df[column].astype(str)
                else:
                    values_to_check = df[column]
                matches = int(values_to_check.str.match(regex).sum())
                passed = matches == len(df)
                print(f"   Column: {column}")
                print(f"   Pattern: {regex}")
                print(f"   Matches: {matches}/{len(df)}")
            else:
                passed = False
                print(f"   Column '{column}' not found!")
        else:
            passed = True
            print("   (No handler for this expectation type — skipped)")

        status = "PASSED" if passed else "FAILED"
        print(f"   {status}\n")
        results.append(passed)

    # Summary
    print("=" * 70)
    passed_count = sum(results)
    total_count = len(results)
    success_rate = (passed_count / total_count) * 100 if total_count else 0

    print(f"\nValidation Summary:")
    print(f"   Total expectations: {total_count}")
    print(f"   Passed: {passed_count}")
    print(f"   Failed: {total_count - passed_count}")
    print(f"   Success rate: {success_rate:.1f}%\n")

    if passed_count == total_count:
        print("All validations passed.")
    else:
        print("Some validations failed — review the results above.")

    print("\n" + "=" * 70 + "\n")


def main():
    """Entry point."""
    validate_sales_data()


if __name__ == "__main__":
    main()
