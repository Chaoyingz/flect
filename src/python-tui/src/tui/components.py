from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class Button(BaseModel):
    ctype: Literal["button"] = "button"

    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = "default"
    size: Literal["default", "sm", "lg", "icon"] = "default"
    children: str


class Avatar(BaseModel):
    ctype: Literal["avatar"] = "avatar"

    src: Optional[str] = None
    alt: Optional[str] = None
    fallback: str


class Container(BaseModel):
    ctype: Literal["container"] = "container"

    className: Optional[str] = None
    components: Optional[list["AnyComponent"]] = None
    tag: Optional[Literal["div", "section", "header", "footer", "main", "nav"]] = None


class Logo(BaseModel):
    ctype: Literal["logo"] = "logo"

    size: Literal["sm", "md", "lg"] = "md"
    text: str


AnyComponent = Annotated[
    Union[Button, Avatar, Container, Logo],
    Field(discriminator="ctype"),
]
