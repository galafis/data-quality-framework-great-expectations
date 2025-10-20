"""
Data Profiling Example with Great Expectations
Author: Gabriel Demetrios Lafis
Description: Demonstrate how to profile data and generate statistics
"""

import pandas as pd
from pathlib import Path


def profile_dataset(csv_path):
    """
    Profile a dataset and display statistics
    
    Args:
        csv_path: Path to the CSV file to profile
    """
    print(f"\n{'='*70}")
    print(f"DATA PROFILING: {csv_path.name}")
    print(f"{'='*70}\n")
    
    # Load data
    df = pd.read_csv(csv_path)
    
    # Basic information
    print("📊 BASIC INFORMATION")
    print("-" * 70)
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
    print(f"Total cells: {len(df) * len(df.columns)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # Column information
    print("\n📋 COLUMN DETAILS")
    print("-" * 70)
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        unique_count = df[col].nunique()
        
        print(f"\n{col}:")
        print(f"  Type: {dtype}")
        print(f"  Null values: {null_count} ({null_pct:.1f}%)")
        print(f"  Unique values: {unique_count}")
        
        # Show statistics for numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"  Min: {df[col].min()}")
            print(f"  Max: {df[col].max()}")
            print(f"  Mean: {df[col].mean():.2f}")
            print(f"  Median: {df[col].median():.2f}")
    
    # Data quality summary
    print("\n✅ DATA QUALITY SUMMARY")
    print("-" * 70)
    total_cells = len(df) * len(df.columns)
    total_nulls = df.isnull().sum().sum()
    completeness = ((total_cells - total_nulls) / total_cells) * 100
    
    print(f"Completeness: {completeness:.2f}%")
    print(f"Total null values: {total_nulls}")
    
    # Detect potential issues
    print("\n⚠️  POTENTIAL ISSUES")
    print("-" * 70)
    issues = []
    
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        if null_pct > 10:
            issues.append(f"  • Column '{col}' has {null_pct:.1f}% null values")
    
    if not issues:
        print("  No significant issues detected! ✓")
    else:
        for issue in issues:
            print(issue)
    
    print("\n" + "=" * 70 + "\n")


def main():
    """
    Main execution function
    """
    # Get project root directory
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    # Profile sales data
    sales_csv = data_dir / "sample_sales.csv"
    if sales_csv.exists():
        profile_dataset(sales_csv)
    else:
        print(f"⚠️  File not found: {sales_csv}")
    
    # Profile customer data
    customers_csv = data_dir / "sample_customers.csv"
    if customers_csv.exists():
        profile_dataset(customers_csv)
    else:
        print(f"⚠️  File not found: {customers_csv}")


if __name__ == "__main__":
    main()
