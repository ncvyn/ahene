import os

from google.genai import types

from functions.helper import validate_path


def get_files_info(working_directory: str, directory="."):
    (is_err, result) = validate_path(working_directory, directory, should_be_dir=True)
    if is_err:
        return result
    target_dir = result

    final_result = ""
    for file_name in os.listdir(target_dir):
        absolute_file = os.path.join(target_dir, file_name)
        file_size = os.path.getsize(absolute_file)
        is_dir = os.path.isdir(absolute_file)
        final_result += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"
    return final_result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
