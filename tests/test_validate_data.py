"""
Unit tests for validate_data.py
Author: Gabriel Demetrios Lafis
"""

import pytest
import sys
from pathlib import Path

# Add notebooks directory to path


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent / "notebooks"))

    from validate_data import validate_sales_data, print_results, main
    from io import StringIO


    class TestValidateSalesData:
        """Tests for the validate_sales_data function."""

        @pytest.fixture
        def csv_path(self):
            return Path(__file__).parent.parent / "data" / "sample_sales.csv"

        @pytest.mark.unit
        def test_returns_list_of_results(self, csv_path):
            """validate_sales_data should return a list of dicts."""
            results = validate_sales_data(csv_path)
            assert isinstance(results, list)
            assert len(results) > 0
            for r in results:
                assert "name" in r
                assert "status" in r
                assert "details" in r

        @pytest.mark.unit
        def test_all_checks_pass_on_sample_data(self, csv_path):
            """Every check should pass on the included sample_sales.csv."""
            results = validate_sales_data(csv_path)
            for r in results:
                assert r["status"] == "PASSED", f"{r['name']} failed: {r['details']}"

        @pytest.mark.unit
        def test_row_count_is_accurate(self, csv_path):
            """Row count check should report the real row count."""
            results = validate_sales_data(csv_path)
            row_check = next(r for r in results if r["name"] == "Row Count Check")
            assert "10 rows" in row_check["details"]

        @pytest.mark.unit
        def test_file_not_found(self, tmp_path):
            """Should return a FAILED result when the file does not exist."""
            fake_path = tmp_path / "missing.csv"
            results = validate_sales_data(fake_path)
            assert results[0]["status"] == "FAILED"
            assert "not found" in results[0]["details"]

        @pytest.mark.unit
        def test_expected_check_names(self, csv_path):
            """Should include all expected check names."""
            results = validate_sales_data(csv_path)
            names = {r["name"] for r in results}
            expected = {
                "Row Count Check",
                "Null Check - Order ID",
                "Unique Check - Order ID",
                "Null Check - Customer ID",
                "Sales Range Check",
                "Quantity Range Check",
                "Discount Range Check",
                "Category Values",
                "Ship Mode Values",
                "Date Format Check",
            }
            assert expected.issubset(names)


    class TestPrintResults:
        """Tests for the print_results helper."""

        @pytest.mark.unit
        def test_print_results_output(self):
            """print_results should write a readable summary to stdout."""
            results = [
                {"name": "Check A", "status": "PASSED", "details": "ok"},
                {"name": "Check B", "status": "FAILED", "details": "bad"},
            ]
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                print_results(results)
                output = sys.stdout.getvalue()
                assert "Check A" in output
                assert "Check B" in output
                assert "1/2 checks passed" in output
            finally:
                sys.stdout = old_stdout


    class TestMain:
        """Integration test — main() should run without errors."""

        @pytest.mark.unit
        def test_main_runs(self):
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                main()
                output = sys.stdout.getvalue()
                assert "Summary" in output
            finally:
                sys.stdout = old_stdout
