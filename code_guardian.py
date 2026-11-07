
import ast
import sys

from enum import Enum, auto


class Flow(Enum):
    RETURN = auto()
    RAISE = auto()
    FALLTHROUGH = auto()
    BREAK = auto()
    CONTINUE = auto()

def analyze_sequence(statements):
    outcomes = {Flow.FALLTHROUGH}

    for statement in statements:
        if Flow.FALLTHROUGH not in outcomes:
            break

        outcomes.remove(Flow.FALLTHROUGH)

        if isinstance(statement, ast.Return):
            outcomes.add(Flow.RETURN)

        elif isinstance(statement, ast.Raise):
            outcomes.add(Flow.RAISE)

        elif isinstance(statement, ast.Break):
            outcomes.add(Flow.BREAK)

        elif isinstance(statement, ast.Continue):
            outcomes.add(Flow.CONTINUE)

        elif isinstance(statement, (ast.For, ast.AsyncFor)):
            body_outcomes = analyze_sequence(statement.body)

            loop_outcomes = (
                body_outcomes
                - {Flow.BREAK, Flow.CONTINUE, Flow.FALLTHROUGH}
            )

            if statement.orelse:
                loop_outcomes.update(
                    analyze_sequence(statement.orelse)
                )
            else:
                loop_outcomes.add(Flow.FALLTHROUGH)

            if Flow.BREAK in body_outcomes:
                loop_outcomes.add(Flow.FALLTHROUGH)

            outcomes.update(loop_outcomes)

        elif isinstance(statement, ast.While):
            body_outcomes = analyze_sequence(statement.body)

            loop_outcomes = (
                body_outcomes
                - {Flow.BREAK, Flow.CONTINUE, Flow.FALLTHROUGH}
            )

            if statement.orelse:
                loop_outcomes.update(
                    analyze_sequence(statement.orelse)
            )
            else:
                loop_outcomes.add(Flow.FALLTHROUGH)

            if Flow.BREAK in body_outcomes:
                loop_outcomes.add(Flow.FALLTHROUGH)
            outcomes.update(loop_outcomes)

        elif isinstance(statement, ast.If):
            body_outcomes = analyze_sequence(statement.body)

            else_outcomes = (
                analyze_sequence(statement.orelse)
                if statement.orelse
                else {Flow.FALLTHROUGH}
            )

            outcomes.update(body_outcomes)
            outcomes.update(else_outcomes)

        elif isinstance(statement, (ast.Try, getattr(ast, "TryStar", ast.Try))):
            try_outcomes = analyze_sequence(statement.body)

            for handler in statement.handlers:
                try_outcomes.update(
                    analyze_sequence(handler.body)
                )

            if statement.orelse and Flow.FALLTHROUGH in try_outcomes:
                try_outcomes.remove(Flow.FALLTHROUGH)
                try_outcomes.update(
                    analyze_sequence(statement.orelse)
                )

            if statement.finalbody:
                final_outcomes = analyze_sequence(statement.finalbody)
                combined = set()

                for final_outcome in final_outcomes:
                    if final_outcome == Flow.FALLTHROUGH:
                        combined.update(try_outcomes)
                    else:
                        combined.add(final_outcome)

                try_outcomes = combined

            outcomes.update(try_outcomes)

        else:
            outcomes.add(Flow.FALLTHROUGH)

    return outcomes




def always_terminates(statements):
    for statement in statements:
        if isinstance(statement, (ast.Return, ast.Raise)):
            return True

        if isinstance(statement, ast.If):
            body_terminates = always_terminates(statement.body)
            else_terminates = (
                always_terminates(statement.orelse)
                if statement.orelse
                else False
            )

            if body_terminates and else_terminates:
                return True

        if isinstance(statement, ast.Try):
            body_terminates = always_terminates(statement.body)

            handlers_terminate = all(
                always_terminates(handler.body)
                for handler in statement.handlers
            )

            if body_terminates and handlers_terminate:
                return True

            if statement.finalbody and always_terminates(statement.finalbody):
                return True

    return False




def check_python_file(filename):
    with open(filename, "r", encoding="utf-8-sig") as file:
        source_code = file.read()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as error:
        return [f"Syntax error: {error}"]

    issues = []
        
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_"):
                continue

            if Flow.FALLTHROUGH in analyze_sequence(node.body):
                issues.append(
                    f"Function '{node.name}' may fall through "
                    "without returning or raising."
                )

    return issues


    


    




if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) != 2:
        print("Usage: python code_guardian.py <file_or_folder>")
        raise SystemExit(1)

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"Error: '{target}' does not exist.")
        raise SystemExit(1)

    if target.is_file():
        files = [target] if target.suffix == ".py" else []
    else:
        files = sorted(target.rglob("*.py"))

    if not files:
        print("No Python files found.")
        raise SystemExit(0)

    total_issues = 0

    for file_path in files:
        issues = check_python_file(str(file_path))
        print(f"\nChecking: {file_path}")

        if issues:
            for issue in issues:
                print(f"WARNING: {issue}")
                total_issues += 1
        else:
            print("No issues found.")

    print(f"\nChecked {len(files)} Python file(s).")
    print(f"Found {total_issues} issue(s).")
    raise SystemExit(1 if total_issues > 0 else 0)

