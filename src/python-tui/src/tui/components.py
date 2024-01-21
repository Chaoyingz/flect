import typing as _t

import pydantic as _p


class BaseComponent(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")


class BaseContainerComponent(BaseComponent):
    children: _t.Optional[list["AnyComponent"]] = None


class Button(BaseComponent):
    ctype: _t.Literal["button"] = "button"

    variant: _t.Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = "default"
    size: _t.Literal["default", "sm", "lg", "icon"] = "default"
    children: str


class Avatar(BaseComponent):
    ctype: _t.Literal["avatar"] = "avatar"

    src: _t.Optional[str] = None
    alt: _t.Optional[str] = None
    fallback: str


class Container(BaseContainerComponent):
    ctype: _t.Literal["container"] = "container"

    className: _t.Optional[str] = None
    tag: _t.Optional[_t.Literal["div", "section", "header", "footer", "main", "nav", "aside"]] = None


class Logo(BaseComponent):
    ctype: _t.Literal["logo"] = "logo"

    size: _t.Literal["sm", "md", "lg"] = "md"
    text: str


class Heading(BaseComponent):
    ctype: _t.Literal["heading"] = "heading"

    level: _t.Literal[1, 2, 3, 4, 5, 6]
    text: str
    id: _t.Optional[str] = None


class Link(BaseContainerComponent):
    ctype: _t.Literal["link"] = "link"

    href: str


class Text(BaseComponent):
    ctype: _t.Literal["text"] = "text"

    text: str


AnyComponent = _t.Annotated[
    _t.Union[Button, Avatar, Container, Logo, Heading, Link, Text],
    _p.Field(discriminator="ctype"),
]


# Rebuild forward ref models
for container_component in BaseContainerComponent.__subclasses__():
    container_component.model_rebuild()
