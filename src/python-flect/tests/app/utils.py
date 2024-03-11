import pathlib

APP_PATH = pathlib.Path(__file__).parent


def get_relative_path_text(file: str) -> str:
    file_path = pathlib.Path(file)
    relative_path = file_path.relative_to(APP_PATH)
    return convert_path_to_regex_str(str(relative_path))


def convert_path_to_regex_str(path: str) -> str:
    return f"^{path}$"
