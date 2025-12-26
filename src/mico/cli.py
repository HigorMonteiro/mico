"""Command-line interface for Mico."""

import sys
from typing import Optional


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for the mico CLI.

    Args:
        args: Command-line arguments. If None, uses sys.argv[1:].

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    if args is None:
        args = sys.argv[1:]

    if not args:
        print("Mico - macOS System Monitoring CLI")
        print("\nUsage: mico [command] [options]")
        print("\nCommands:")
        print("  --version    Show version information")
        print("  --help       Show this help message")
        return 0

    if "--version" in args or "-v" in args:
        from mico import __version__
        print(f"mico {__version__}")
        return 0

    if "--help" in args or "-h" in args:
        print("Mico - macOS System Monitoring CLI")
        print("\nUsage: mico [command] [options]")
        print("\nCommands:")
        print("  --version    Show version information")
        print("  --help       Show this help message")
        return 0

    print(f"Unknown command: {' '.join(args)}")
    print("Use 'mico --help' for usage information.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

