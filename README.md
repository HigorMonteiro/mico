# Mico

CLI tool for monitoring macOS systems.

## Overview

Mico is a command-line interface designed to monitor and track system metrics, performance, and health status of macOS computers.

## Features

- System monitoring
- Performance metrics tracking
- Health status reporting
- Real-time system information

## Installation

### From PyPI (when published)

```bash
pip install mico
```

### From source

```bash
git clone <repository-url>
cd mico
pip install -e .
```

### Development installation

```bash
git clone <repository-url>
cd mico
pip install -e ".[dev]"
```

## Usage

```bash
# Show version
mico --version

# Show help
mico --help

# Run monitoring commands (to be implemented)
mico monitor
```

## Requirements

- macOS 10.13+ (High Sierra or later)
- Python 3.8 or higher

## Development

### Setup development environment

```bash
# Clone the repository
git clone <repository-url>
cd mico

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Building the package

```bash
# Build source distribution
python -m build --sdist

# Build wheel
python -m build --wheel

# Build both
python -m build
```

### Publishing to PyPI

```bash
# Build the package
python -m build

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

## Project Structure

```
mico/
├── src/
│   └── mico/
│       ├── __init__.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_cli.py
├── pyproject.toml
├── setup.py
└── README.md
```

## License

MIT License

