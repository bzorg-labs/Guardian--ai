import ast
from code_guardian import analyze_sequence, Flow

from code_guardian import check_python_file


def test_function_with_missing_return(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def check_number(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    else:\n'
        '        if n < 0:\n'
        '            return "negative"\n',
        encoding="utf-8",
    )

    issues = check_python_file(str(sample))
    assert len(issues) == 1


def test_function_missing_return_in_one_branch(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    else:\n'
        '        print("not positive")\n',
        encoding="utf-8",
    )

    issues = check_python_file(str(sample))
    assert len(issues) == 1


def test_both_branches_return(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    else:\n'
        '        return "not positive"\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []


def test_return_after_if(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    return "not positive"\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []


def test_syntax_error(tmp_path):
    sample = tmp_path / "broken.py"
    sample.write_text(
        "def broken(:\n    return 1\n",
        encoding="utf-8",
    )

    issues = check_python_file(str(sample))
    assert len(issues) == 1
    assert "Syntax error" in issues[0]


def test_if_without_else_followed_by_print(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    print("not positive")\n',
        encoding="utf-8",
    )

    assert len(check_python_file(str(sample))) == 1


def test_elif_without_else_has_missing_return(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(n):\n'
        '    if n > 0:\n'
        '        return "positive"\n'
        '    elif n < 0:\n'
        '        return "negative"\n',
        encoding="utf-8",
    )

    assert len(check_python_file(str(sample))) == 1


def test_return_inside_loop_may_not_cover_all_paths(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(items):\n'
        '    for item in items:\n'
        '        return item\n',
        encoding="utf-8",
    )

    assert len(check_python_file(str(sample))) == 1


def test_return_after_loop(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example(items):\n'
        '    for item in items:\n'
        '        print(item)\n'
        '    return "done"\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []
def test_try_except_both_branches_return(tmp_path):
    sample = tmp_path / "sample.py"
    sample.write_text(
        'def example():\n'
        '    try:\n'
        '        return 1\n'
        '    except ValueError:\n'
        '        return 0\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []

def test_try_finally_with_return(tmp_path):
    sample = tmp_path / "sample.py"

    sample.write_text(
        'def calculate():\n'
        '    try:\n'
        '        return 100\n'
        '    finally:\n'
        '        print("Done")\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []

def test_try_finally_return_overrides_return(tmp_path):
    sample = tmp_path / "sample.py"

    sample.write_text(
        'def calculate():\n'
        '    try:\n'
        '        return 100\n'
        '    finally:\n'
        '        return 200\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []

def test_try_return_without_except_and_finally_print(tmp_path):
    sample = tmp_path / "sample.py"

    sample.write_text(
        'def calculate():\n'
        '    try:\n'
        '        return 100\n'
        '    finally:\n'
        '        print("Done")\n'
        '    print("Unreachable")\n',
        encoding="utf-8",
    )

    assert check_python_file(str(sample)) == []

def test_analyze_if_both_branches_terminate():
    tree = ast.parse(
        "def f(x):\n"
        "    if x > 0:\n"
        "        return 10\n"
        "    else:\n"
        "        raise ValueError()\n"
    )

    outcomes = analyze_sequence(tree.body[0].body)

    assert outcomes == {Flow.RETURN, Flow.RAISE}


def test_analyze_if_without_else():
    tree = ast.parse(
        "def f(x):\n"
        "    if x > 0:\n"
        "        return 10\n"
    )

    outcomes = analyze_sequence(tree.body[0].body)

    assert outcomes == {Flow.RETURN, Flow.FALLTHROUGH}

def test_try_finally_mixed_paths():
    source = """
def calculate(x):
    try:
        if x > 0:
            return 10
    finally:
        if x < 0:
            return 20
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert Flow.RETURN in outcomes
    assert Flow.FALLTHROUGH in outcomes

def test_finally_return_overrides_fallthrough():
    source = """
def calculate():
    try:
        pass
    finally:
        return 20
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert outcomes == {Flow.RETURN}

def test_finally_raise_overrides_return():
    source = """
def calculate():
    try:
        return 10
    finally:
        raise ValueError("failed")
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert outcomes == {Flow.RAISE}

def test_for_loop_with_return_and_break():
    source = """
def calculate(items):
    for item in items:
        if item > 0:
            return item
        break
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert Flow.RETURN in outcomes
    assert Flow.FALLTHROUGH in outcomes

def test_for_loop_continue_does_not_end_function():
    source = """
def calculate(items):
    for item in items:
        if item > 0:
            continue
        return item
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert Flow.RETURN in outcomes
    assert Flow.FALLTHROUGH in outcomes

def test_for_loop_else_without_break():
    source = """
def calculate(items):
    for item in items:
        if item > 0:
            return item
    else:
        return 0
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert outcomes == {Flow.RETURN}

def test_for_loop_break_skips_else():
    source = """
def calculate(items):
    for item in items:
        break
    else:
        return 100
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert Flow.FALLTHROUGH in outcomes
    assert Flow.FALLTHROUGH in outcomes

def test_while_loop_may_not_execute():
    source = """
def calculate(x):
    while x > 0:
        return 10
"""
    tree = ast.parse(source)
    function = tree.body[0]

    outcomes = analyze_sequence(function.body)

    assert Flow.RETURN in outcomes
    assert Flow.FALLTHROUGH in outcomes