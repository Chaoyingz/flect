from html import escape
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny, model_validator
from typing_extensions import Self


class BaseComponent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    class_name: Optional[str] = Field(
        None, description="The tailwind class names of the component.", serialization_alias="className"
    )

    def render_to_html(self) -> str:
        return ""


class BaseContainerComponent(BaseComponent):
    children: Optional[list["AnyComponent"]] = Field(
        None,
        description="The children of the component.",
    )


class Avatar(BaseComponent):
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

    def render_to_html(self) -> str:
        return f"""\
        <img
            src="{escape(self.src or "")}"
            alt="{escape(self.alt or "")}"
        />
        <span>{escape(self.fallback)}</span>
        """


class Button(BaseComponent):
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

    def render_to_html(self) -> str:
        return f"""\
        <button>
            {escape(self.children)}
        </button>
        """


class Container(BaseContainerComponent):
    ctype: Literal["container"] = "container"

    tag: Literal["div", "section", "header", "footer", "main", "nav", "aside"] = Field(
        "div",
        description="The tag of the container.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <{self.tag}>
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </{self.tag}>
        """


class Heading(BaseComponent):
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

    def render_to_html(self) -> str:
        return f"""\
        <h{self.level}>
            {escape(self.text)}
        </h{self.level}>
        """


class Link(BaseContainerComponent):
    ctype: Literal["link"] = "link"

    href: str = Field(
        ...,
        description="The href of the link.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <a href="{escape(self.href)}">
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </a>
        """


class Outlet(BaseComponent):
    ctype: Literal["outlet"] = "outlet"


class Table(BaseComponent):
    ctype: Literal["table"] = "table"

    labels: list[str] = Field(
        [],
        description="The labels of the table, defaults to the keys of the dataset.",
    )
    datasets: list[SerializeAsAny[BaseModel]] = Field(
        ...,
        description="The datasets of the table.",
    )

    @model_validator(mode="after")
    def set_default_labels(self) -> Self:
        if not self.labels:
            self.labels = list(self.datasets[0].model_fields.keys())
        return self

    def render_to_html(self) -> str:
        return f"""\
        <table>
            <thead>
                <tr>
                    {"".join(f"<th>{escape(label)}</th>" for label in self.labels)}
                </tr>
            </thead>
            <tbody>
                {"".join(f"<tr>{''.join(f'<td>{escape(getattr(dataset, label))}</td>' for label in self.labels)}</tr>" for dataset in self.datasets)}
            </tbody>
        </table>
        """


class Text(BaseComponent):
    ctype: Literal["text"] = "text"

    text: str = Field(
        ...,
        description="The text of the text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <p>{escape(self.text)}</p>
        """


AnyComponent = Annotated[
    Union[Avatar, Button, Container, Heading, Link, Outlet, Table, Text],
    Field(discriminator="ctype"),
]

# Rebuild forward ref models
for container_component in BaseContainerComponent.__subclasses__():
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
)
