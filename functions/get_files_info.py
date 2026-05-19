import os


def get_files_info(working_directory, directory="."):
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir, directory))
    valid_target_dir = os.path.commonpath([working_dir, target_dir]) == working_dir
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    return f'Success: "{directory}" is within the working directory'
