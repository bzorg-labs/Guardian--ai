# GUARDIAN — MASTER CONTEXT

**Project:** AI Code Guardian  
**Repository:** `bzorg-labs/Guardian--ai`  
**Local path:** `C:\Users\User\Desktop\Guardian--ai`  
**Purpose:** Build a reliable Python code analyzer that detects potential defects before code is merged.

---

## 1. Project Vision

Guardian is an AI Code Guardian designed to evaluate, test, and judge AI-generated code before merge.

Long-term direction:
- Static code analysis
- Control-flow analysis
- Automated testing with pytest
- Risk scoring
- AI-assisted code review and patch suggestions
- CI integration with GitHub Actions

**Important:** The current product is an early prototype. Do not describe it as a complete or production-ready AI code reviewer.

## 2. Current Development Stage

The current focus is a Python static analyzer that detects functions that may reach their end without an explicit `return` or `raise`.

Main technical concepts:
- Python AST (`ast`)
- `FunctionDef`
- `Return` and `Raise`
- `If`, `Try`, `ExceptHandler`, `Finally`
- Execution paths
- Control flow
- Recursive analysis
- pytest regression tests

## 3. Current Files

- `code_guardian.py` — main analyzer
- `test_guardian.py` — automated tests
- `run_guardian.py` — runner
- `README.md` — project documentation
- `sample.py`, `sample_bad.py`, and other sample files — test inputs

## 4. Current Algorithm

The main function currently under development:

`always_terminates(statements)`

Its purpose is to determine whether all relevant execution paths through a sequence of statements terminate through `return` or `raise`.

Current known limitations:
- Complex `try/except/finally` behavior is not fully modeled.
- Exception paths are not exhaustively analyzed.
- Loops require more precise control-flow reasoning.
- Nested control structures need systematic testing.

Do not claim sound or complete control-flow analysis yet.

## 5. Latest Verified Test Status

Last reported command:

`python -m pytest -q`

Last reported output:

`13 passed in 0.31s`

A test for `try/finally` was proposed but has NOT yet been confirmed as added.

Proposed regression case:

```python
def calculate():
    try:
        return 100
    finally:
        print("Done")
```

Expected behavior: Guardian should report no missing-return issue.

Before changing the algorithm:
1. Add the regression test.
2. Run pytest.
3. Confirm the bug.
4. Fix the implementation.
5. Run the full test suite again.

Never remove existing tests just to make a new test pass.

## 6. Technical Rules

- Write a failing test before fixing a bug.
- Preserve all existing tests.
- Avoid large rewrites without evidence.
- Explain the reason for each algorithmic change.
- Test edge cases.
- Do not claim support for behavior that has not been tested.
- Keep the prototype small and reliable.

## 7. Development Environment

- Windows
- PowerShell
- VS Code
- Python 3.14.2
- pytest 9.2.0

Run tests from the Guardian directory:

```powershell
cd "$HOME\Desktop\Guardian--ai"
python -m pytest -q
```

Compile-check:

```powershell
python -m py_compile .\code_guardian.py
```

## 8. Teaching and Collaboration Style

The user has a BSc in Software Engineering and strong mathematical foundations.

Teaching requirements:
- Explain mechanisms, not just syntax.
- Use Persian for the main explanation.
- Preserve English technical terms and explain their meaning.
- Explain why the code works and what Python does internally.
- Avoid repetitive beginner quizzes.
- Move at a serious pace while ensuring conceptual understanding.
- Give one concrete next action at a time.
- Do not confuse the Guardian project with the separate TorchVision project in `C:\Users\User\vision`.

## 9. Business and Delivery Priorities

Guardian must become a real portfolio and income opportunity, not an endless learning exercise.

Priorities:
1. Build a reliable minimal product.
2. Demonstrate its value with real code examples and regression tests.
3. Publish a clear GitHub portfolio.
4. Explore potential users and paid pilot opportunities.
5. Expand toward AI-assisted code review and CI integration.

Avoid unnecessary features that delay a usable MVP.

## 10. Session Handoff Protocol

At the end of each substantial work session, update this document with:

- Date
- Current implementation status
- Files changed
- Tests added or modified
- Latest test result
- Known bugs and limitations
- Decisions made
- Exact next action

When starting a new ChatGPT conversation, provide this file and say:

**"Continue Guardian from this master context. First inspect the current status and continue from the exact next action. Do not restart the project or repeat completed work."**

---

**Core rule:** Preserve project continuity. Do not make the user repeat established decisions or rebuild completed work.