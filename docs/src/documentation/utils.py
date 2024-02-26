from documentation import CONTENT_DIR


def get_markdown_content(filename: str) -> str:
    with open(CONTENT_DIR / filename) as f:
        return f.read()
