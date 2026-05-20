import os

from functions.helper import validate_path


def write_file(working_directory: str, file_path: str, content: str) -> str:
    (is_err, result) = validate_path(
        working_directory, file_path, should_be_dir=False, create_if_empty=True
    )
    if is_err:
        return result

    file = result
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file}" ({len(content)} characters written)'
