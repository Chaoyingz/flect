import typing as _t

import pydantic as _p


class _BaseComponent(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")

    className: _t.Optional[str] = None


class _BaseContainerComponent(_BaseComponent):
    children: _t.Optional[list["AnyComponent"]] = None


class Avatar(_BaseComponent):
    ctype: _t.Literal["avatar"] = "avatar"

    src: _t.Optional[str] = None
    alt: _t.Optional[str] = None
    fallback: str


class Button(_BaseComponent):
    ctype: _t.Literal["button"] = "button"

    variant: _t.Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = "default"
    size: _t.Literal["default", "sm", "lg", "icon"] = "default"
    children: str


class Container(_BaseContainerComponent):
    ctype: _t.Literal["container"] = "container"

    tag: _t.Optional[_t.Literal["div", "section", "header", "footer", "main", "nav", "aside"]] = None


class Heading(_BaseComponent):
    ctype: _t.Literal["heading"] = "heading"

    level: _t.Literal[1, 2, 3, 4, 5, 6]
    text: str
    id: _t.Optional[str] = None


class Link(_BaseContainerComponent):
    ctype: _t.Literal["link"] = "link"

    href: str


class Text(_BaseComponent):
    ctype: _t.Literal["text"] = "text"

    text: str


AnyComponent = _t.Annotated[
    _t.Union[Avatar, Button, Container, Heading, Link, Text],
    _p.Field(discriminator="ctype"),
]
AnyComponents = list[AnyComponent]

# Rebuild forward ref models
for container_component in _BaseContainerComponent.__subclasses__():
    container_component.model_rebuild()


__all__ = (
    "Avatar",
    "Button",
    "Container",
    "Heading",
    "Link",
    "Text",
    "AnyComponent",
    "AnyComponents",
)
