
import ast
import sys







def always_terminates(statements):
    for statement in statements:
        if isinstance(statement, (ast.Return, ast.Raise)):
            return True

        if isinstance(statement, ast.If):
            body_terminates = always_terminates(statement.body)

            if statement.orelse:
                else_terminates = always_terminates(statement.orelse)
            else:
                else_terminates = False

            if body_terminates and else_terminates:
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

            if not always_terminates(node.body):
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

