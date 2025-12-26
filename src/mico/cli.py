"""Command-line interface for Mico."""

import sys
from mico import __version__
import click
from mico.adapters.system import SystemAdapter
from mico.domain.use_cases.list_processes import ListProcessesUseCase
from mico.domain.use_cases.filter_processes import FilterProcessesUseCase


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


@cli.command()
@click.option(
    "--top",
    "-t",
    default=10,
    type=int,
    help="Number of processes to display (default: 10)"
)
@click.option(
    "--sort",
    "-s",
    type=click.Choice(["mem", "name", "pid"], case_sensitive=False),
    default="mem",
    help="Sort criteria: mem (memory), name, or pid (default: mem)"
)
@click.option(
    "--filter",
    "-f",
    default="",
    help="Filter processes by name or PID"
)
def top(top: int, sort: str, filter: str):
    """
    Display top processes by memory consumption.
    
    Examples:
    
      # Top 10 processes by memory
      mico top
      
      # Top 20 processes sorted by name
      mico top --top 20 --sort name
      
      # Filter Chrome processes
      mico top --filter chrome
    """
    adapter = SystemAdapter()
    all_processes = adapter.get_all_processes()
    
    if not all_processes:
        click.echo("No processes found.")
        return
    
    filtered_processes = FilterProcessesUseCase.execute(all_processes, filter)
    
    if not filtered_processes:
        click.echo(f"No processes found matching filter: {filter}")
        return
    
    sorted_processes = ListProcessesUseCase.execute(
        filtered_processes,
        sort_by=sort,
        reverse=True,
        top_n=top
    )
    
    click.echo(f"\n📊 Top {len(sorted_processes)} Processes (sorted by {sort})\n")
    click.echo(f"{'PID':<8} {'Name':<30} {'Memory (MB)':<15} {'Memory (%)':<12} {'User'}")
    click.echo("-" * 85)
    
    for process in sorted_processes:
        memory_mb = process.memory.rss_mb
        memory_percent = process.memory.percent or 0.0
        username = process.username or "N/A"
        name = process.name[:28] + ".." if len(process.name) > 30 else process.name
        
        click.echo(
            f"{process.pid:<8} {name:<30} {memory_mb:>12.2f} MB {memory_percent:>10.2f}%  {username}"
        )
    
    click.echo()


if __name__ == "__main__":
    cli()
