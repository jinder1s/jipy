#!/usr/bin/env python
"""Tests for `jipy` package."""
from jipy.jipy import jipy, run_file, run_prompt, run, error, report
from unittest.mock import patch
import pytest

@patch('jipy.jipy.run_file')
@patch('jipy.jipy.path')
def test_jipy_run_file(mock_path, mock_run_file):
    # test run_file is called when path to a file is passed to function
    mock_path.isfile.return_value = True
    jipy(["random_path"])
    mock_run_file.assert_called()


@patch('jipy.jipy.run_prompt')
def test_jipy_run_file(mock_run_prompt):
    # test run_prompt is called when passed no value
    jipy([])
    mock_run_prompt.assert_called()

def test_jipy_run_files():
    # Jipy should error out if too many values inputted
    with pytest.raises(Exception) as contest:
        jipy(['1', '2'])
