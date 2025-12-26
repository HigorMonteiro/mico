"""Tests for CLI module."""

import pytest
from mico.cli import main


def test_main_version():
    """Test version command."""
    result = main(["--version"])
    assert result == 0


def test_main_help():
    """Test help command."""
    result = main(["--help"])
    assert result == 0


def test_main_no_args():
    """Test main with no arguments."""
    result = main([])
    assert result == 0


def test_main_unknown_command():
    """Test main with unknown command."""
    result = main(["unknown"])
    assert result == 1

