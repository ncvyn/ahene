import os

from google.genai import types

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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file that is located in the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path that points to the file to (over)write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file.",
            ),
        },
    ),
)
