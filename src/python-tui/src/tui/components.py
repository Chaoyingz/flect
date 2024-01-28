import typing as _t

import pydantic as _p


class _BaseComponent(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")

    class_name: _t.Optional[str] = _p.Field(
        None, description="The tailwind class names of the component.", serialization_alias="className"
    )


class _BaseContainerComponent(_BaseComponent):
    children: _t.Optional[list["AnyComponent"]] = _p.Field(
        None,
        description="The children of the component.",
    )


class Avatar(_BaseComponent):
    ctype: _t.Literal["avatar"] = "avatar"

    src: _t.Optional[str] = _p.Field(
        None,
        description="The source of the avatar.",
    )
    alt: _t.Optional[str] = _p.Field(
        None,
        description="The alternative text of the avatar.",
    )
    fallback: str = _p.Field(
        ...,
        description="The fallback text of the avatar.",
    )


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

    level: _t.Literal[1, 2, 3, 4, 5, 6] = _p.Field(
        ...,
        description="The level of the heading.",
    )
    text: str = _p.Field(
        ...,
        description="The text of the heading.",
    )
    id: _t.Optional[str] = _p.Field(
        None,
        description="The id of the heading.",
    )


class Link(_BaseContainerComponent):
    ctype: _t.Literal["link"] = "link"

    href: str = _p.Field(
        ...,
        description="The href of the link.",
    )


class Outlet(_BaseComponent):
    ctype: _t.Literal["outlet"] = "outlet"


class Table(_BaseComponent):
    ctype: _t.Literal["table"] = "table"

    labels: list[str] = _p.Field(
        [],
        description="The labels of the table, defaults to the keys of the dataset.",
    )
    datasets: list[_p.SerializeAsAny[_p.BaseModel]] = _p.Field(
        ...,
        description="The datasets of the table.",
    )

    @_p.model_validator(mode="before")
    @classmethod
    def set_default_labels(cls, values: _t.Any) -> _t.Any:
        if not values.get("labels"):
            values["labels"] = list(values["datasets"][0].model_fields.keys())
        return values


class Text(_BaseComponent):
    ctype: _t.Literal["text"] = "text"

    text: str = _p.Field(
        ...,
        description="The text of the text.",
    )


AnyComponent = _t.Annotated[
    _t.Union[Avatar, Button, Container, Heading, Link, Outlet, Table, Text],
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
    "Outlet",
    "Table",
    "Text",
    "AnyComponent",
    "AnyComponents",
)
