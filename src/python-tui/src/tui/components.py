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
    tag: Optional[Literal["div", "section", "header", "footer", "main", "nav", "aside"]] = None


class Logo(BaseModel):
    ctype: Literal["logo"] = "logo"

    size: Literal["sm", "md", "lg"] = "md"
    text: str


class Heading(BaseModel):
    ctype: Literal["heading"] = "heading"

    level: Literal[1, 2, 3, 4, 5, 6]
    text: str
    id: Optional[str] = None


class Link(BaseModel):
    ctype: Literal["link"] = "link"

    href: str
    text: str
    className: Optional[str] = None


AnyComponent = Annotated[
    Union[Button, Avatar, Container, Logo, Heading, Link],
    Field(discriminator="ctype"),
]
