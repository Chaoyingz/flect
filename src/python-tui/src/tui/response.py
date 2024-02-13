from typing import Optional, Union

from pydantic import BaseModel, Field

from tui.components import AnyComponent


class MetaTitleTemplate(BaseModel):
    _outlet = "%t%"

    template: str = Field(..., description="The template of the title.")
    default: str = Field(..., description="The default title.")
    absolute: bool = Field(False, description="Determines if the title is absolute.")


class Meta(BaseModel):
    title: Union[str, MetaTitleTemplate, None] = Field(None, description="The document title.")
    description: Optional[str] = Field(None, description="Standard metadata names.")
    keywords: Optional[str] = Field(None, description="The keywords for the document.")


class Response(BaseModel):
    meta: Optional[Meta] = Field(None, description="The metadata of the response.")
    element: Optional[AnyComponent] = Field(None, description="The components of the response.")
