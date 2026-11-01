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