import os


# Returns a tuple containing
# is_err (bool)
# result (str)
def validate_path(
    working_directory: str,
    relative_path: str,
    should_be_dir: bool,
    create_if_empty=False,
) -> tuple[bool, str]:
    abs_working_dir = os.path.abspath(working_directory)
    path = os.path.normpath(os.path.join(abs_working_dir, relative_path))

    if should_be_dir:
        is_path_dir = os.path.isdir(path)
        if not is_path_dir:
            return (True, f'Error: "{path}" is not an existing directory')
    elif not should_be_dir and not create_if_empty:
        is_path_file = os.path.isfile(path)
        if not is_path_file:
            return (True, f'Error: "{path}" is not an existing file')

    valid_target_directory = (
        os.path.commonpath([abs_working_dir, path]) == abs_working_dir
    )
    if not valid_target_directory:
        return (
            True,
            f'Error: "{path}" is outside the permitted working directory',
        )

    return (False, path)
