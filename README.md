# AI Code Guardian

A lightweight, rule-based static analysis tool for Python.

Guardian uses Python's built-in AST module to identify potential
incomplete return paths without executing source code.

## Features

- Python syntax error detection
- Basic return-path analysis
- Conditional branch analysis
- Recursive directory scanning
- Command-line interface
- Non-zero exit codes when issues are detected
- Automated tests with pytest
- GitHub Actions integration

## Installation

Clone the repository:

    git clone https://github.com/bzorg-labs/Guardian--ai.git
    cd Guardian--ai

## Usage

Analyze a Python file:

    python code_guardian.py sample.py

Analyze a directory:

    python code_guardian.py path/to/project

## Tests

Install pytest:

    python -m pip install pytest

Run tests:

    python -m pytest -v

## Limitations

Guardian is an early prototype. Its current analysis is rule-based
and does not fully understand all Python control-flow structures.

Complex loops, exception handling, and some nested structures
may produce false positives or false negatives.

Guardian is not a replacement for a mature static-analysis tool.

## Project Status

Early prototype. Under active development.

## Author

bzorg-labs
https://github.com/bzorg-labs
