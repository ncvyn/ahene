from functions.get_files_info import get_files_info

test_parameters = [".", "pkg", "/bin", "../"]
for parameter in test_parameters:
    print(
        f"Result for {'current' if parameter == '.' else f"'{parameter}'"} directory:"
    )
    result = get_files_info("calculator", parameter)
    print(result.replace("- ", "  - ").replace("Error: ", "    Error: "))
