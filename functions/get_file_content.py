from config import MAX_CHARS
from functions.helper import validate_path


def get_file_content(working_directory: str, file_path: str) -> str:
    (is_err, result) = validate_path(working_directory, file_path, should_be_dir=False)
    if is_err:
        return result

    full_file_path = result
    with open(full_file_path, "r") as f:
        file_content = f.read(MAX_CHARS)
        if f.read(1):
            file_content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return file_content
