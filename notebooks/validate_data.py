"""
Data Quality Validation Script
Author: Gabriel Demetrios Lafis
Description: Validates sample CSV data using pandas — checks for nulls,
             type correctness, value ranges, allowed categories, and date formats.
"""

import pandas as pd
from pathlib import Path
import re


def validate_sales_data(csv_path):
    """
    Run data quality checks against a sales CSV file using pandas.

    Returns a list of check result dicts with keys: name, status, details.
    """
    results = []

    if not csv_path.exists():
        results.append({
            "name": "File Exists",
            "status": "FAILED",
            "details": f"File not found: {csv_path}",
        })
        return results

    df = pd.read_csv(csv_path)
    row_count = len(df)

    # --- Row Count ---
    results.append({
        "name": "Row Count Check",
        "status": "PASSED" if row_count > 0 else "FAILED",
        "details": f"{row_count} rows found",
    })

    # --- Null Check: order_id ---
    null_order = int(df["order_id"].isnull().sum())
    results.append({
        "name": "Null Check - Order ID",
        "status": "PASSED" if null_order == 0 else "FAILED",
        "details": f"{null_order} null values" if null_order else "No nulls found",
    })

    # --- Uniqueness: order_id ---
    dup_count = row_count - df["order_id"].nunique()
    results.append({
        "name": "Unique Check - Order ID",
        "status": "PASSED" if dup_count == 0 else "FAILED",
        "details": f"{dup_count} duplicates" if dup_count else "All values unique",
    })

    # --- Null Check: customer_id ---
    null_cust = int(df["customer_id"].isnull().sum())
    results.append({
        "name": "Null Check - Customer ID",
        "status": "PASSED" if null_cust == 0 else "FAILED",
        "details": f"{null_cust} null values" if null_cust else "No nulls found",
    })

    # --- Sales Range (>= 0) ---
    bad_sales = int((df["sales"].dropna() < 0).sum())
    results.append({
        "name": "Sales Range Check",
        "status": "PASSED" if bad_sales == 0 else "FAILED",
        "details": f"{bad_sales} negative values" if bad_sales else "All values >= 0",
    })

    # --- Quantity Range (>= 1) ---
    bad_qty = int((df["quantity"].dropna() < 1).sum())
    results.append({
        "name": "Quantity Range Check",
        "status": "PASSED" if bad_qty == 0 else "FAILED",
        "details": f"{bad_qty} values below 1" if bad_qty else "All values >= 1",
    })

    # --- Discount Range (0-1) ---
    disc = df["discount"].dropna()
    bad_disc = int(((disc < 0) | (disc > 1)).sum())
    results.append({
        "name": "Discount Range Check",
        "status": "PASSED" if bad_disc == 0 else "FAILED",
        "details": f"{bad_disc} out-of-range values" if bad_disc else "All values between 0 and 1",
    })

    # --- Category Values ---
    valid_categories = {"Furniture", "Office Supplies", "Technology"}
    invalid_cats = set(df["category"].dropna().unique()) - valid_categories
    results.append({
        "name": "Category Values",
        "status": "PASSED" if not invalid_cats else "FAILED",
        "details": f"Invalid: {invalid_cats}" if invalid_cats else "All valid categories",
    })

    # --- Ship Mode Values ---
    valid_ship = {"Standard Class", "Second Class", "First Class", "Same Day"}
    invalid_ship = set(df["ship_mode"].dropna().unique()) - valid_ship
    results.append({
        "name": "Ship Mode Values",
        "status": "PASSED" if not invalid_ship else "FAILED",
        "details": f"Invalid: {invalid_ship}" if invalid_ship else "All valid ship modes",
    })

    # --- Date Format (MM/DD/YYYY) ---
    date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    date_ok = df["order_date"].dropna().apply(lambda x: bool(date_pattern.match(str(x))))
    bad_dates = int((~date_ok).sum())
    results.append({
        "name": "Date Format Check",
        "status": "PASSED" if bad_dates == 0 else "FAILED",
        "details": f"{bad_dates} malformed dates" if bad_dates else "All dates match MM/DD/YYYY",
    })

    return results


def print_results(results):
    """Print validation results to stdout."""
    print("\nData Quality Validation Results")
    print("-" * 60)

    for check in results:
        symbol = "PASS" if check["status"] == "PASSED" else "FAIL"
        print(f"[{symbol}] {check['name']}: {check['details']}")

    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    print("-" * 60)
    print(f"Summary: {passed}/{total} checks passed")
    print("=" * 60)


def main():
    """
    Load sample_sales.csv and run data quality checks.
    """
    project_root = Path(__file__).parent.parent
    csv_path = project_root / "data" / "sample_sales.csv"

    results = validate_sales_data(csv_path)
    print_results(results)


if __name__ == "__main__":
    main()
