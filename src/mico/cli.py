"""Command-line interface for Mico."""

import sys
from mico import __version__
import click
from mico.adapters.system import SystemAdapter


@click.group()
@click.version_option(version=__version__, prog_name="mico")
def cli():
    """Mico - macOS System Monitoring CLI."""
    pass


@cli.command()
def memory():
    """Display system memory information."""
    adapter = SystemAdapter()
    system_info = adapter.get_system_info()
    memory_info = system_info.memory
    
    click.echo("\n💾 System Memory Information\n")
    click.echo(f"Total:      {memory_info.total_gb:.2f} GB ({memory_info.total_mb:.0f} MB)")
    click.echo(f"Used:       {memory_info.used_gb:.2f} GB ({memory_info.used_mb:.0f} MB)")
    click.echo(f"Available:  {memory_info.available_gb:.2f} GB ({memory_info.available_mb:.0f} MB)")
    click.echo(f"Free:       {memory_info.free_gb:.2f} GB ({memory_info.free_mb:.0f} MB)")
    click.echo(f"Usage:      {memory_info.percent:.1f}%\n")


if __name__ == "__main__":
    cli()
