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


def test_cli_top_command():
    """Test top command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["top", "--top", "5"])
    assert result.exit_code == 0
    assert "Processes" in result.output or "processes" in result.output.lower()


def test_cli_top_command_with_filter():
    """Test top command with filter."""
    runner = CliRunner()
    result = runner.invoke(cli, ["top", "--filter", "python", "--top", "3"])
    assert result.exit_code in [0, 1]


def test_cli_health_command():
    """Test health command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0
    assert "Health" in result.output or "health" in result.output.lower()
    assert "Score" in result.output or "score" in result.output.lower()
