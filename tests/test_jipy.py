#!/usr/bin/env python
"""Tests for `jipy` package."""
from jipy.jipy import Jipy
from unittest.mock import patch, Mock
import pytest


@patch("jipy.jipy.path")
def test_jipy_run_file(mock_path):
    # test run_file is called when path to a file is passed to function
    mock_run_file = Mock()
    jipy = Jipy()
    jipy.run_file = mock_run_file
    mock_path.isfile.return_value = True
    jipy.jipy(["random_path"])
    mock_run_file.assert_called()


def test_jipy_run_prompt():
    # test run_prompt is called when passed no value
    mock_run_prompt = Mock()
    jipy = Jipy()
    jipy.run_prompt = mock_run_prompt
    jipy.jipy([])
    mock_run_prompt.assert_called()


def test_jipy_invalid_input():
    jipy = Jipy()
    # Jipy should error out if too many values inputted
    with pytest.raises(Exception) as contest:
        jipy.jipy(["1", "2"])


def test_jipy_run():
    jipy = Jipy()
    source = "true == true"
    jipy.run(source)


def test_jipy_run2():
    jipy = Jipy()
    source = "(true == true)"
    jipy.run(source)
