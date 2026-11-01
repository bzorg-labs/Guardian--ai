
from code_guardian import check_python_file

issues = check_python_file("sample.py")

if issues:
    for issue in issues:
        print("WARNING:", issue)
else:
    print("No issues found.")
