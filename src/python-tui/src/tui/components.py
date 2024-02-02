from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, model_validator


class _BaseComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    class_name: Optional[str] = Field(
        None, description="The tailwind class names of the component.", serialization_alias="className"
    )


class _BaseContainerComponent(_BaseComponent):
    children: Optional[list["AnyComponent"]] = Field(
        None,
        description="The children of the component.",
    )


class Avatar(_BaseComponent):
    ctype: Literal["avatar"] = "avatar"

    src: Optional[str] = Field(
        None,
        description="The source of the avatar.",
    )
    alt: Optional[str] = Field(
        None,
        description="The alternative text of the avatar.",
    )
    fallback: str = Field(
        ...,
        description="The fallback text of the avatar.",
    )


class Button(_BaseComponent):
    ctype: Literal["button"] = "button"

    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = Field(
        "default",
        description="The variant of the button.",
    )
    size: Literal["default", "sm", "lg", "icon"] = Field(
        "default",
        description="The size of the button.",
    )
    children: str


class Container(_BaseContainerComponent):
    ctype: Literal["container"] = "container"

    tag: Optional[Literal["div", "section", "header", "footer", "main", "nav", "aside"]] = None


class Heading(_BaseComponent):
    ctype: Literal["heading"] = "heading"

    level: Literal[1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="The level of the heading.",
    )
    text: str = Field(
        ...,
        description="The text of the heading.",
    )
    id: Optional[str] = Field(
        None,
        description="The id of the heading.",
    )


class Link(_BaseContainerComponent):
    ctype: Literal["link"] = "link"

    href: str = Field(
        ...,
        description="The href of the link.",
    )


class Outlet(_BaseComponent):
    ctype: Literal["outlet"] = "outlet"


class Table(_BaseComponent):
    ctype: Literal["table"] = "table"

    labels: list[str] = Field(
        [],
        description="The labels of the table, defaults to the keys of the dataset.",
    )
    datasets: list[SerializeAsAny[BaseModel]] = Field(
        ...,
        description="The datasets of the table.",
    )

    @model_validator(mode="before")
    @classmethod
    def set_default_labels(cls, values: Any) -> Any:
        if not values.get("labels"):
            values["labels"] = list(values["datasets"][0].model_fields.keys())
        return values


class Text(_BaseComponent):
    ctype: Literal["text"] = "text"

    text: str = Field(
        ...,
        description="The text of the text.",
    )


AnyComponent = Annotated[
    Union[Avatar, Button, Container, Heading, Link, Outlet, Table, Text],
    Field(discriminator="ctype"),
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
