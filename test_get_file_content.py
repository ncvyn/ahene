from functions.get_file_content import get_file_content

test_parameters = [
    "lorem.txt",
    "main.py",
    "pkg/calculator.py",
    "/bin/cat",
    "pkg/does_not_exist.py",
]
for parameter in test_parameters:
    result = get_file_content("calculator", parameter)
    print(f"{parameter} length: {len(result)}")
    print(f"{parameter} truncated: {'truncated' in result}")
    if parameter != "lorem.txt":
        print(result)
