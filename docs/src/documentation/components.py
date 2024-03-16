import pathlib
from typing import Literal, Optional

import pyromark
from flect import components as c
from typing_extensions import Self


class BaseUIComponent(c.Custom):
    package: Literal["docs-ui"] = "docs-ui"
    sub_type: Literal["badge"] = "markdown"


class Markdown(BaseUIComponent):
    class_name: Optional[str] = None
    text: str

    def render_to_html(self) -> str:
        return f"""\
        {pyromark.markdown(self.text)}
        """

    @classmethod
    def from_file(cls, path: pathlib.Path, class_name: Optional[str] = None) -> Self:
        try:
            return cls(text=path.read_text(), class_name=class_name)
        except FileNotFoundError:
            return cls(text="Markdown file not found.", class_name=class_name)
