import typing as _t

import pydantic as _p


class _BaseComponent(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")

    className: _t.Optional[str] = _p.Field(
        None,
        description="The tailwind class names of the component.",
    )


class _BaseContainerComponent(_BaseComponent):
    children: _t.Optional[list["AnyComponent"]] = _p.Field(
        None,
        description="The children of the component.",
    )


class Avatar(_BaseComponent):
    ctype: _t.Literal["avatar"] = "avatar"

    src: _t.Optional[str] = None
    alt: _t.Optional[str] = None
    fallback: str


class Button(_BaseComponent):
    ctype: _t.Literal["button"] = "button"

    variant: _t.Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = _p.Field(
        "default",
        description="The variant of the button.",
    )
    size: _t.Literal["default", "sm", "lg", "icon"] = _p.Field(
        "default",
        description="The size of the button.",
    )
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


class Table(_BaseComponent):
    ctype: _t.Literal["table"] = "table"

    labels: list[str] = []
    datasets: list[_p.SerializeAsAny[_p.BaseModel]]

    @_p.model_validator(mode="before")
    @classmethod
    def set_default_labels(cls, values: _t.Any) -> _t.Any:
        if not values.get("labels"):
            values["labels"] = list(values["datasets"][0].model_fields.keys())
        return values


class Text(_BaseComponent):
    ctype: _t.Literal["text"] = "text"

    text: str


AnyComponent = _t.Annotated[
    _t.Union[Avatar, Button, Container, Heading, Link, Table, Text],
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
