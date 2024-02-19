from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Self

from tui.actions import AnyAction
from tui.components import AnyComponent


class TitleTemplate(BaseModel):
    template: Optional[str] = Field(None, description="The template of the title.")
    default: str = Field(..., description="The default title.")
    absolute: bool = Field(False, description="Determines if the title is absolute.")

    def apply_parent_title(self, parent_title: Union[Self, str, None]) -> None:
        if parent_title is None or self.absolute:
            return

        if isinstance(parent_title, str):
            parent_title_template = TitleTemplate(
                template=None,
                default=parent_title,
                absolute=False,
            )
        else:
            parent_title_template = parent_title

        if parent_title_template.template:
            self.default = parent_title_template.template.format(title=self.default)
        else:
            self.default = f"{self.default} - {parent_title_template.default}"

        self.absolute = parent_title_template.absolute


class Meta(BaseModel):
    title: Union[str, TitleTemplate, None] = Field(None, description="The document title.")
    description: Optional[str] = Field(None, description="Standard metadata names.")
    keywords: Optional[str] = Field(None, description="The keywords for the document.")

    @field_validator("title")
    def validate_title(cls, value: Union[str, TitleTemplate, None]) -> Union[TitleTemplate, None]:
        if isinstance(value, str):
            return TitleTemplate(template=None, default=value, absolute=False)
        return value

    def render_to_html(self) -> str:
        html = ""

        if self.title is not None:
            assert isinstance(self.title, TitleTemplate)
            html += f"<title>{self.title.default}</title>"

        if self.description is not None:
            html += f'<meta name="description" content="{self.description}">'

        if self.keywords is not None:
            html += f'<meta name="keywords" content="{self.keywords}">'

        return html


def merge_meta(meta: Optional[Meta], other: Optional[Meta]) -> Optional[Meta]:
    if meta is None:
        return other
    if other is None:
        return meta
    assert isinstance(meta.title, TitleTemplate)
    assert isinstance(other.title, TitleTemplate)
    meta.title = meta.title or other.title
    meta.description = meta.description or other.description
    meta.keywords = meta.keywords or other.keywords
    if meta.title and not meta.title.absolute:
        meta.title.apply_parent_title(other.title)
    return meta


class PageResponse(BaseModel):
    meta: Optional[Meta] = Field(None, description="The metadata of the response.")
    element: Optional[AnyComponent] = Field(None, description="The components of the response.")


class ActionResponse(BaseModel):
    action: AnyAction
