import os
import subprocess

from google.genai import types

from config import TIMEOUT
from functions.helper import validate_path


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    if file_path.split(".")[-1] != "py":
        return f'Error: "{file_path}" is not a Python file'
    (is_err, result) = validate_path(working_directory, file_path, should_be_dir=False)
    if is_err:
        return result
    abs_path = result

    command = ["python", abs_path]
    if args:
        command.extend(args)
    abs_cwd = os.path.dirname(abs_path)

    try:
        cmd_result = subprocess.run(
            command, cwd=abs_cwd, capture_output=True, text=True, timeout=TIMEOUT
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = ""
    if cmd_result.returncode != 0:
        output += f"Process exited with code {cmd_result.returncode}\n"
    if cmd_result.stdout == "" and cmd_result.stderr == "":
        output += "No output produced\n"
    else:
        if cmd_result.stdout != "":
            output += f"STDOUT:\n{cmd_result.stdout}(stdout end)\n"
        else:
            output += f"STDERR:\n{cmd_result.stderr}(stderr end)\n"
    return output


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file with optional arguments sent to it. If the file does so, the function also outputs STDOUT and STDERR. It also returns the process code if the command was unsucessful",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get content from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="[THIS IS OPTIONAL] A list of arguments (args) that will be sent to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="[THIS IS OPTIONAL] An argument that will be sent to the Python file.",
                ),
            ),
        },
    ),
)
