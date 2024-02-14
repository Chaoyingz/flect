from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Self

from tui.components import AnyComponent


class TitleTemplate(BaseModel):
    template: Optional[str] = Field(None, description="The template of the title.")
    default: str = Field(..., description="The default title.")
    absolute: bool = Field(False, description="Determines if the title is absolute.")

    def apply_parent_title(self, parent_title: Union[Self, str, None]) -> None:
        if parent_title is None or self.absolute:
            return

        if isinstance(parent_title, str):
            parent_title = TitleTemplate(default=parent_title)

        if parent_title.template:
            self.default = parent_title.template.format(title=self.default)
        else:
            self.default = f"{self.default} - {parent_title.default}"

        self.absolute = parent_title.absolute


class Meta(BaseModel):
    title: Union[str, TitleTemplate, None] = Field(None, description="The document title.")
    description: Optional[str] = Field(None, description="Standard metadata names.")
    keywords: Optional[str] = Field(None, description="The keywords for the document.")

    @field_validator("title")
    def validate_title(cls, value: Union[str, TitleTemplate, None]) -> Union[TitleTemplate, None]:
        if isinstance(value, str):
            return TitleTemplate(default=value)
        return value

    def render_to_html(self) -> str:
        html = ""

        if self.title is not None:
            html += f"<title>{self.title.default}</title>"

        if self.description is not None:
            html += f'<meta name="description" content="{self.description}">'

        if self.keywords is not None:
            html += f'<meta name="keywords" content="{self.keywords}">'

        return html


class Response(BaseModel):
    meta: Optional[Meta] = Field(None, description="The metadata of the response.")
    element: Optional[AnyComponent] = Field(None, description="The components of the response.")
