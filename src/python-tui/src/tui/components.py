from html import escape
from typing import Annotated, Literal, Optional, Union

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, SerializeAsAny, field_serializer, model_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Self


class BaseComponent(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=AliasGenerator(serialization_alias=to_camel))

    class_name: Optional[str] = Field(
        None,
        description="The tailwind class names of the component.",
    )

    def render_to_html(self) -> str:
        return ""


class BaseContainerComponent(BaseComponent):
    children: Optional[list["AnyComponent"]] = Field(
        None,
        description="The children of the component.",
    )


class Avatar(BaseComponent):
    component_type: Literal["avatar"] = "avatar"

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
    component_type: Literal["button"] = "button"

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
    component_type: Literal["container"] = "container"

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


class Form(BaseComponent):
    component_type: Literal["form"] = "form"
    model: type[BaseModel] = Field(
        ...,
        description="The model of the form.",
    )
    submit_method: Literal["POST", "PUT", "PATCH"] = Field(
        "POST",
        description="The submit method of the form.",
    )
    submit_url: str = Field(
        ...,
        description="The submit url of the form.",
    )

    @field_serializer("model")
    def serialize_model(self, model: type[BaseModel]) -> dict:
        return model.model_json_schema()


class Heading(BaseComponent):
    component_type: Literal["heading"] = "heading"

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
    component_type: Literal["link"] = "link"

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


class NavLink(BaseContainerComponent):
    component_type: Literal["nav-link"] = "nav-link"

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
    component_type: Literal["outlet"] = "outlet"


class Table(BaseComponent):
    component_type: Literal["table"] = "table"

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
    component_type: Literal["text"] = "text"

    text: str = Field(
        ...,
        description="The text of the text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <p>{escape(self.text)}</p>
        """


AnyComponent = Annotated[
    Union[Avatar, Button, Container, Form, Heading, Link, NavLink, Outlet, Table, Text],
    Field(discriminator="component_type"),
]

# Rebuild forward ref models
for container_component in BaseContainerComponent.__subclasses__():
    container_component.model_rebuild()


__all__ = (
    "Avatar",
    "Button",
    "Container",
    "Form",
    "Heading",
    "Link",
    "NavLink",
    "Outlet",
    "Table",
    "Text",
    "AnyComponent",
)
