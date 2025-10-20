"""
Tests for Great Expectations configuration files
Author: Gabriel Demetrios Lafis
"""

import pytest
import json
from pathlib import Path


class TestExpectationsSuite:
    """Test suite for Great Expectations suite configuration"""
    
    @pytest.fixture
    def sales_suite_path(self):
        """Get path to sales data suite"""
        return Path(__file__).parent.parent / "great_expectations" / "expectations" / "sales_data_suite.json"
    
    @pytest.fixture
    def sales_suite(self, sales_suite_path):
        """Load sales data suite"""
        with open(sales_suite_path, 'r') as f:
            return json.load(f)
    
    @pytest.mark.unit
    def test_sales_suite_exists(self, sales_suite_path):
        """Test that sales data suite file exists"""
        assert sales_suite_path.exists()
        assert sales_suite_path.is_file()
    
    @pytest.mark.unit
    def test_sales_suite_is_valid_json(self, sales_suite):
        """Test that sales suite is valid JSON"""
        assert isinstance(sales_suite, dict)
    
    @pytest.mark.unit
    def test_sales_suite_has_required_fields(self, sales_suite):
        """Test that sales suite has all required fields"""
        assert "expectation_suite_name" in sales_suite
        assert "data_asset_type" in sales_suite
        assert "expectations" in sales_suite
        assert "meta" in sales_suite
    
    @pytest.mark.unit
    def test_sales_suite_name(self, sales_suite):
        """Test that sales suite has correct name"""
        assert sales_suite["expectation_suite_name"] == "sales_data_quality_suite"
    
    @pytest.mark.unit
    def test_sales_suite_has_expectations(self, sales_suite):
        """Test that sales suite has expectations defined"""
        expectations = sales_suite["expectations"]
        assert isinstance(expectations, list)
        assert len(expectations) > 0
    
    @pytest.mark.unit
    def test_sales_suite_expectations_structure(self, sales_suite):
        """Test that each expectation has correct structure"""
        for expectation in sales_suite["expectations"]:
            assert "expectation_type" in expectation
            assert "kwargs" in expectation
            assert expectation["expectation_type"].startswith("expect_")
    
    @pytest.mark.unit
    def test_sales_suite_has_row_count_check(self, sales_suite):
        """Test that suite includes row count validation"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_table_row_count_to_be_between" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_has_null_checks(self, sales_suite):
        """Test that suite includes null value checks"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_column_values_to_not_be_null" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_has_uniqueness_check(self, sales_suite):
        """Test that suite includes uniqueness validation"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_column_values_to_be_unique" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_has_value_set_checks(self, sales_suite):
        """Test that suite includes value set validation"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_column_values_to_be_in_set" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_has_range_checks(self, sales_suite):
        """Test that suite includes range validation"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_column_values_to_be_between" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_has_regex_checks(self, sales_suite):
        """Test that suite includes regex pattern validation"""
        expectation_types = [e["expectation_type"] for e in sales_suite["expectations"]]
        assert "expect_column_values_to_match_regex" in expectation_types
    
    @pytest.mark.unit
    def test_sales_suite_metadata(self, sales_suite):
        """Test that suite has proper metadata"""
        meta = sales_suite["meta"]
        assert "great_expectations_version" in meta
        assert "author" in meta
        assert meta["author"] == "Gabriel Demetrios Lafis"
    
    @pytest.mark.unit
    def test_sales_suite_validates_order_id(self, sales_suite):
        """Test that order_id column has proper validations"""
        order_id_expectations = [
            e for e in sales_suite["expectations"]
            if e.get("kwargs", {}).get("column") == "order_id"
        ]
        assert len(order_id_expectations) > 0
        
        # Check for both null and uniqueness checks
        types = [e["expectation_type"] for e in order_id_expectations]
        assert "expect_column_values_to_not_be_null" in types
        assert "expect_column_values_to_be_unique" in types
    
    @pytest.mark.unit
    def test_sales_suite_validates_sales_range(self, sales_suite):
        """Test that sales column has range validation"""
        sales_expectations = [
            e for e in sales_suite["expectations"]
            if e.get("kwargs", {}).get("column") == "sales"
        ]
        assert len(sales_expectations) > 0
        
        # Check that range is positive
        for exp in sales_expectations:
            if exp["expectation_type"] == "expect_column_values_to_be_between":
                assert exp["kwargs"]["min_value"] >= 0
