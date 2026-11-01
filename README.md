# Guardian AI

**AI Code Guardian — A rule-based static analysis tool for Python**

## 👋 About Me

Hi, I'm **bzorg-labs**.

I'm building Guardian, a Python static analysis tool designed to identify potential issues in code, especially incomplete return paths and control-flow problems.

## 🎯 Project Goals

- Detect functions that may finish without returning a value or raising an exception.
- Analyze conditional branches and return paths.
- Report Python syntax errors.
- Build a foundation for more advanced control-flow and exception-flow analysis.

## 🛠️ Current Features

- Python source parsing with the `ast` module.
- File and directory scanning.
- Rule-based warnings for potentially incomplete return paths.
- Automated tests with `pytest`.

## 🔬 Current Focus

- Improving return-path analysis.
- Expanding test coverage with edge cases.
- Reducing false positives.
- Exploring exception flow and more advanced control-flow reasoning.

## 💡 Philosophy

I learn by building small tools, testing ideas, and documenting the engineering process.

## 📍 Status

**Early prototype — actively developing and testing.**