# Guardian — AI Code Guardian

**Lightweight Python control-flow analysis for catching potentially incomplete return paths before code reaches production.**

Guardian is a Python static-analysis prototype that uses Python's built-in `ast` module to inspect function control flow without executing the code.

## The Problem

Functions with incomplete return paths can produce unexpected `None` values and subtle bugs.

Guardian checks Python functions for potentially incomplete return paths and reports issues before code is merged.

## How It Works

- Parses Python source code using the built-in AST module.
- Analyzes selected control-flow structures.
- Detects functions that may reach the end without returning or raising an exception.
- Supports text and JSON reports.
- Returns a non-zero exit code when issues are detected, making it usable in CI workflows.

## Quick Start

Requirements:
- Python 3.14
- pytest (for running tests)

Clone the repository:

```bash
git clone https://github.com/bzorg-labs/Guardian--ai.git
cd Guardian--ai
```

Run Guardian against a Python file:

```bash
python code_guardian.py code_guardian.py
```

Generate a JSON report:

```bash
python code_guardian.py code_guardian.py --format json
```

Run the test suite:

```bash
python -m pytest -q
```

## Example

Consider this function:

```python
def calculate(value):
    if value > 0:
        return value
```

When `value` is zero or negative, the function reaches the end without an explicit return.

Guardian reports:

```text
Function 'calculate' may fall through without returning or raising.
```

## GitHub Actions Integration

Guardian can run as part of a GitHub Actions workflow.

It uses exit codes to indicate whether potential issues were detected, allowing CI workflows to fail when Guardian finds a problem.

## Current Limitations

Guardian is an early-stage prototype.

- Its control-flow analysis is limited to supported Python constructs.
- It does not prove program correctness.
- It does not replace mature static-analysis tools such as Pyright, Ruff, or Pylint.
- It does not execute code or perform runtime testing.

## Project Status

Early prototype — under active development.

## Author

**bzorg-labs**

https://github.com/bzorg-labs
