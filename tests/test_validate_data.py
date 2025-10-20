"""
Unit tests for validate_data.py script
Author: Gabriel Demetrios Lafis
"""

import pytest
import sys
from pathlib import Path
from io import StringIO

# Add notebooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "notebooks"))

from validate_data import main


class TestValidateData:
    """Test suite for validate_data module"""
    
    @pytest.mark.unit
    def test_main_executes_without_errors(self):
        """Test that main function executes without errors"""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            main()
            output = sys.stdout.getvalue()
            
            # Check that expected output is present
            assert "Initializing Great Expectations" in output
            assert "Data Quality Validation Complete!" in output
            assert "✓" in output or "PASSED" in output
        finally:
            sys.stdout = old_stdout
    
    @pytest.mark.unit
    def test_main_prints_check_results(self):
        """Test that main function prints check results"""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            main()
            output = sys.stdout.getvalue()
            
            # Check that all expected checks are present
            assert "Row Count Check" in output
            assert "Null Check - Order ID" in output
            assert "Sales Range Check" in output
            assert "Category Values" in output
            assert "Date Format" in output
        finally:
            sys.stdout = old_stdout
    
    @pytest.mark.unit
    def test_main_shows_passed_status(self):
        """Test that all checks show PASSED status"""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            main()
            output = sys.stdout.getvalue()
            
            # Check that all checks pass
            assert output.count("PASSED") >= 5
            assert "FAILED" not in output
        finally:
            sys.stdout = old_stdout
    
    @pytest.mark.unit
    def test_main_displays_separator_lines(self):
        """Test that output includes formatting"""
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            main()
            output = sys.stdout.getvalue()
            
            # Check for separator lines
            assert "-" * 60 in output
            assert "=" * 60 in output
        finally:
            sys.stdout = old_stdout
