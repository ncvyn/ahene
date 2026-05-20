import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    full_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    valid_file_path = os.path.isfile(full_file_path)
    if not valid_file_path:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    valid_target_directory = (
        os.path.commonpath([abs_working_dir, full_file_path]) == abs_working_dir
    )
    if not valid_target_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(full_file_path, "r") as f:
        file_content = f.read(MAX_CHARS)
        if f.read(1):
            file_content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return file_content
