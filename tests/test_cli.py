"""Tests for CLI module."""

import pytest
from click.testing import CliRunner
from mico.cli import cli


def test_cli_version():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "mico" in result.output.lower()


def test_cli_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "mico" in result.output.lower()


def test_cli_memory_command():
    """Test memory command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["memory"])
    assert result.exit_code == 0
    assert "Memory" in result.output or "memory" in result.output.lower()
