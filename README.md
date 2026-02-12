# Data Quality Framework with Great Expectations

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A demonstration framework for data quality validation concepts. The project ships with sample CSV data, a Great Expectations–compatible expectation suite (JSON), and Python scripts that run the validations using **pandas**.

> **Note:** The validation scripts in `notebooks/` use pandas directly rather than the Great Expectations runtime. The expectation suite JSON follows the GX format so it can also be loaded by Great Expectations if you install it separately.

---

## What's Included

| Component | Description |
|-----------|-------------|
| `great_expectations/expectations/sales_data_suite.json` | Expectation suite defining checks for the sales dataset |
| `notebooks/validate_data.py` | Standalone validation script — loads `sample_sales.csv` and runs null, range, type, and format checks with pandas |
| `notebooks/example_great_expectations.py` | Reads the expectation suite JSON and executes each expectation against the data using pandas |
| `notebooks/example_profiling.py` | Profiles every CSV in `data/` — row counts, column types, nulls, descriptive stats |
| `data/sample_sales.csv` | 10-row sample of order/sales data |
| `data/sample_customers.csv` | 10-row sample of customer data |
| `tests/` | pytest suite covering the validation scripts and the expectation suite structure |

## Repository Structure

```
data-quality-framework-great-expectations/
├── great_expectations/
│   └── expectations/
│       └── sales_data_suite.json
├── notebooks/
│   ├── validate_data.py
│   ├── example_great_expectations.py
│   └── example_profiling.py
├── data/
│   ├── sample_sales.csv
│   └── sample_customers.csv
├── tests/
│   ├── __init__.py
│   ├── test_validate_data.py
│   └── test_expectations.py
├── images/
│   └── quality_workflow.png
├── .gitignore
├── pytest.ini
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/galafis/data-quality-framework-great-expectations.git
cd data-quality-framework-great-expectations
pip install -r requirements.txt
```

### Run the Scripts

```bash
# Basic validation (pandas)
python notebooks/validate_data.py

# Suite-based validation (reads the JSON expectation suite, validates with pandas)
python notebooks/example_great_expectations.py

# Data profiling
python notebooks/example_profiling.py
```

### Run Tests

```bash
pytest -v
```

## Expectation Suite

The file `great_expectations/expectations/sales_data_suite.json` defines the following checks for `sample_sales.csv`:

| Expectation | Target |
|-------------|--------|
| `expect_table_row_count_to_be_between` | 1 – 100 000 rows |
| `expect_column_values_to_not_be_null` | `order_id`, `customer_id`, `category` |
| `expect_column_values_to_be_unique` | `order_id` |
| `expect_column_values_to_be_in_set` | `ship_mode`, `category` |
| `expect_column_values_to_be_between` | `sales` (0–100 000), `quantity` (1–1 000), `discount` (0–1) |
| `expect_column_values_to_match_regex` | `order_date` (MM/DD/YYYY) |

The suite follows the standard Great Expectations JSON format. If you install `great-expectations` (`pip install great-expectations`), you can load the suite with the GX runtime as well.

## How Validation Works

Both `validate_data.py` and `example_great_expectations.py` perform real checks against the CSV data:

- **Null checks** — `df[column].isnull().sum()`
- **Uniqueness** — compare `nunique()` to row count
- **Range checks** — filter values outside min/max
- **Set membership** — `isin()` against allowed values
- **Regex matching** — `str.match()` on date columns

These are the same logical checks that Great Expectations would perform; the difference is that these scripts run them with pandas without requiring the GX runtime.

## Data Quality Concepts

This project demonstrates several core data quality dimensions:

| Dimension | How It's Checked |
|-----------|-----------------|
| **Completeness** | Null value checks on required columns |
| **Uniqueness** | Duplicate detection on primary keys |
| **Validity** | Value-set and range checks |
| **Consistency** | Regex pattern matching on dates |
| **Accuracy** | Range bounds on numeric fields |

## Using Great Expectations Directly

If you want to use the full GX runtime instead of the pandas-based scripts:

```bash
pip install great-expectations
```

```python
import great_expectations as gx

context = gx.get_context()

# Load the existing suite
suite = context.get_expectation_suite("sales_data_quality_suite")

# Configure a datasource and run a checkpoint
# See https://docs.greatexpectations.io/ for details.
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — see [LICENSE](LICENSE).

---

**Author:** Gabriel Demetrios Lafis
