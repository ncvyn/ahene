import os
import subprocess

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
