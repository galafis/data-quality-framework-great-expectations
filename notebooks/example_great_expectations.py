"""
Great Expectations Integration Example
Author: Gabriel Demetrios Lafis
Description: Demonstrate how to use Great Expectations with real data validation
"""

import pandas as pd
from pathlib import Path
import json


def validate_sales_data():
    """
    Validate sales data using Great Expectations suite definitions
    """
    print("\n" + "="*70)
    print("GREAT EXPECTATIONS - SALES DATA VALIDATION")
    print("="*70 + "\n")
    
    # Load data
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "sample_sales.csv"
    suite_path = project_root / "great_expectations" / "expectations" / "sales_data_suite.json"
    
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        return
    
    if not suite_path.exists():
        print(f"❌ Expectation suite not found: {suite_path}")
        return
    
    # Load data
    df = pd.read_csv(data_path)
    print(f"📊 Loaded {len(df)} rows from {data_path.name}")
    
    # Load expectation suite
    with open(suite_path, 'r') as f:
        suite = json.load(f)
    
    print(f"📋 Loaded expectation suite: {suite['expectation_suite_name']}")
    print(f"   Expectations count: {len(suite['expectations'])}\n")
    
    # Simulate validation (in real scenario, you'd use GX context)
    print("🔍 RUNNING VALIDATIONS:\n")
    
    results = []
    
    for idx, expectation in enumerate(suite['expectations'], 1):
        exp_type = expectation['expectation_type']
        kwargs = expectation.get('kwargs', {})
        
        print(f"{idx}. {exp_type}")
        
        # Simulate validation results
        if exp_type == "expect_table_row_count_to_be_between":
            min_val = kwargs.get('min_value', 0)
            max_val = kwargs.get('max_value', float('inf'))
            passed = min_val <= len(df) <= max_val
            print(f"   Expected: {min_val} - {max_val} rows")
            print(f"   Actual: {len(df)} rows")
            
        elif exp_type == "expect_column_values_to_not_be_null":
            column = kwargs.get('column')
            null_count = df[column].isnull().sum()
            passed = null_count == 0
            print(f"   Column: {column}")
            print(f"   Null values: {null_count}")
            
        elif exp_type == "expect_column_values_to_be_unique":
            column = kwargs.get('column')
            duplicates = len(df) - df[column].nunique()
            passed = duplicates == 0
            print(f"   Column: {column}")
            print(f"   Unique values: {df[column].nunique()}/{len(df)}")
            
        elif exp_type == "expect_column_values_to_be_in_set":
            column = kwargs.get('column')
            value_set = kwargs.get('value_set', [])
            invalid = df[~df[column].isin(value_set)][column].nunique()
            passed = invalid == 0
            print(f"   Column: {column}")
            print(f"   Valid values: {value_set}")
            print(f"   Invalid values found: {invalid}")
            
        elif exp_type == "expect_column_values_to_be_between":
            column = kwargs.get('column')
            if column in df.columns:
                min_val = kwargs.get('min_value')
                max_val = kwargs.get('max_value')
                # Filter out NaN values before range check
                valid_values = df[column].dropna()
                out_of_range = valid_values[(valid_values < min_val) | (valid_values > max_val)].count()
                passed = out_of_range == 0
                print(f"   Column: {column}")
                print(f"   Expected range: {min_val} - {max_val}")
                print(f"   Out of range values: {out_of_range}")
            else:
                passed = False
                print(f"   Column '{column}' not found!")
                
        elif exp_type == "expect_column_values_to_match_regex":
            column = kwargs.get('column')
            regex = kwargs.get('regex')
            if column in df.columns:
                # Only convert to string if not already a string type
                if not pd.api.types.is_string_dtype(df[column]):
                    values_to_check = df[column].astype(str)
                else:
                    values_to_check = df[column]
                matches = values_to_check.str.match(regex).sum()
                passed = matches == len(df)
                print(f"   Column: {column}")
                print(f"   Pattern: {regex}")
                print(f"   Matches: {matches}/{len(df)}")
            else:
                passed = False
                print(f"   Column '{column}' not found!")
        else:
            passed = True
            print(f"   (Skipped in this demo)")
        
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}\n")
        results.append(passed)
    
    # Summary
    print("="*70)
    passed_count = sum(results)
    total_count = len(results)
    success_rate = (passed_count / total_count) * 100
    
    print(f"\n📈 VALIDATION SUMMARY:")
    print(f"   Total expectations: {total_count}")
    print(f"   Passed: {passed_count}")
    print(f"   Failed: {total_count - passed_count}")
    print(f"   Success rate: {success_rate:.1f}%\n")
    
    if passed_count == total_count:
        print("🎉 ALL VALIDATIONS PASSED! Data quality is excellent!")
    else:
        print("⚠️  SOME VALIDATIONS FAILED! Review data quality issues.")
    
    print("\n" + "="*70 + "\n")


def main():
    """
    Main execution function
    """
    print("\n" + "🚀 "*35)
    print("GREAT EXPECTATIONS - DATA QUALITY VALIDATION FRAMEWORK")
    print("🚀 "*35)
    
    validate_sales_data()
    
    print("\n💡 TIP: In production, use Great Expectations SDK directly:")
    print("   import great_expectations as gx")
    print("   context = gx.get_context()")
    print("   results = context.run_checkpoint('your_checkpoint')\n")


if __name__ == "__main__":
    main()
