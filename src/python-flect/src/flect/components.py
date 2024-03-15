import pathlib
import re
from html import escape
from typing import Annotated, Literal, Optional, Type, Union

import pyromark
from pydantic import (
    AliasGenerator,
    BaseModel,
    ConfigDict,
    Field,
    SerializeAsAny,
    WrapSerializer,
    field_serializer,
    model_validator,
)
from pydantic.alias_generators import to_camel
from pydantic_core.core_schema import SerializerFunctionWrapHandler
from typing_extensions import Self

from flect.actions import AnyAction


class BaseComponent(BaseModel):
    package: Literal["flect"] = "flect"
    model_config = ConfigDict(extra="forbid", alias_generator=AliasGenerator(serialization_alias=to_camel))

    class_name: Optional[str] = Field(
        default=None,
        description="Specifies the Tailwind CSS classes for the component.",
    )

    def render_to_html(self) -> str:
        return ""


class BaseContainerComponent(BaseComponent):
    children: Optional[list["AnyComponent"]] = Field(
        default=None,
        description="Defines the child components.",
    )


class Avatar(BaseComponent):
    type: Literal["avatar"] = "avatar"

    src: Optional[str] = Field(
        default=None,
        description="Specifies the image source for the avatar.",
    )
    alt: Optional[str] = Field(
        default=None,
        description="Provides alternative text for the avatar image.",
    )
    fallback: str = Field(
        ...,
        description="Defines the fallback text for the avatar image.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <img
            src="{escape(self.src or "")}"
            alt="{escape(self.alt or "")}"
        />
        <span>{escape(self.fallback)}</span>
        """


class Button(BaseContainerComponent):
    type: Literal["button"] = "button"

    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = Field(
        default="default",
        description="Determines the button's style variant.",
    )
    size: Literal["default", "sm", "lg", "icon"] = Field(
        default="default",
        description="Determines the button's size.",
    )
    on_click_action: Optional[AnyAction] = Field(
        default=None,
        description="Defines the action to be performed when the button is clicked.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <button>
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </button>
        """


class CodeBlock(BaseComponent):
    type: Literal["code-block"] = "code-block"
    text: str = Field(
        ...,
        description="Specifies the code text.",
    )
    language: Optional[str] = Field(
        default=None,
        description="Defines the programming language for syntax highlighting.",
    )
    code_style: Optional[str] = Field(
        default=None,
        description="Determines the code block's style.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <pre>
            <code>
                {escape(self.text)}
            </code>
        </pre>
        """


class Container(BaseContainerComponent):
    type: Literal["container"] = "container"

    tag: Literal["div", "section", "header", "footer", "main", "nav", "aside"] = Field(
        default="div",
        description="Specifies the HTML tag for the container.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <{self.tag}>
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </{self.tag}>
        """


class CopyButton(BaseComponent):
    type: Literal["copy-button"] = "copy-button"
    text: str = Field(
        ...,
        description="Specifies the button's text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <button>
            {escape(self.text)}
        </button>
        """


class Custom(BaseComponent):
    type: Literal["custom"] = "custom"
    sub_type: str


class Form(BaseComponent):
    type: Literal["form"] = "form"
    model: Type[BaseModel] = Field(
        ...,
        description="Defines the form's data model.",
    )
    submit_method: Literal["POST", "PUT", "PATCH"] = Field(
        default="POST",
        description="Specifies the HTTP method for form submission.",
    )
    submit_url: str = Field(
        ...,
        description="Specifies the URL where the form will be submitted.",
    )
    submit_text: Optional[str] = Field(
        default=None,
        description="Specifies the text for the submit button.",
    )

    @field_serializer("model")
    def serialize_model(self, model: Type[BaseModel]) -> dict:
        return model.model_json_schema()


class Heading(BaseComponent):
    type: Literal["heading"] = "heading"

    level: Literal[1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Determines the heading's level (1-6).",
    )
    text: str = Field(
        ...,
        description="Specifies the heading's text.",
    )
    id: Optional[str] = Field(
        default=None,
        description="Specifies the heading's id.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <h{self.level}>
            {escape(self.text)}
        </h{self.level}>
        """


class Link(BaseContainerComponent):
    type: Literal["link"] = "link"

    href: str = Field(
        ...,
        description="Specifies the URL for the link.",
    )
    underline: Literal["none", "hover", "always"] = Field(
        default="hover",
        description="Determines the link's underline style.",
    )
    target: Literal["_self", "_blank"] = Field(
        default="_self",
        description="Specifies the target for the link.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <a href="{escape(self.href)}" target="{self.target}">
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </a>
        """


class Markdown(BaseComponent):
    type: Literal["markdown"] = "markdown"

    text: str = Field(
        ...,
        description="Specifies the markdown text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        {pyromark.markdown(self.text)}
        """

    @classmethod
    def from_file(cls, path: pathlib.Path, class_name: Optional[str] = None) -> Self:
        try:
            return cls(text=path.read_text(), class_name=class_name)
        except FileNotFoundError:
            return cls(text="Markdown file not found.", class_name=class_name)


class NavLink(BaseContainerComponent):
    type: Literal["nav-link"] = "nav-link"

    href: str = Field(
        ...,
        description="Specifies the URL for the navigation link.",
    )
    underline: Literal["none", "hover", "always"] = Field(
        default="hover",
        description="Determines the link's underline style.",
    )
    target: Literal["_self", "_blank"] = Field(
        default="_self",
        description="Specifies the target for the link.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <a href="{escape(self.href)}" target="{self.target}">
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </a>
        """


class Outlet(BaseComponent):
    type: Literal["outlet"] = "outlet"


class Paragraph(BaseComponent):
    type: Literal["paragraph"] = "paragraph"

    text: str = Field(
        ...,
        description="Specifies the paragraph's text.",
    )

    def render_to_html(self) -> str:
        text = escape(self.text)
        pattern = r"\[(.*?)\]\((.*?)\)"
        html_text = re.sub(pattern, r'<a href="\2">\1</a>', text)
        return f"""\
        <p>
            {html_text}
        </p>
        """


class Table(BaseComponent):
    type: Literal["table"] = "table"

    labels: list[str] = Field(
        default=[],
        description="Defines the table's column labels. Defaults to the keys of the dataset.",
    )
    datasets: list[SerializeAsAny[BaseModel]] = Field(
        ...,
        description="Specifies the table's data.",
    )

    @model_validator(mode="after")
    def set_default_labels(self) -> Self:
        if not self.labels and self.datasets:
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
                {"".join(f"<tr>{''.join(f'<td>{escape(str(getattr(dataset, label)))}</td>' for label in self.labels)}</tr>" for dataset in self.datasets)}
            </tbody>
        </table>
        """


class Text(BaseComponent):
    type: Literal["text"] = "text"

    text: str = Field(
        ...,
        description="Specifies the text content.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <p>{escape(self.text)}</p>
        """


COMPONENT_DISCRIMINATOR_NAME = "type"
AnyComponentType = Annotated[
    Union[
        Avatar,
        Button,
        CodeBlock,
        Container,
        CopyButton,
        Custom,
        Form,
        Heading,
        Link,
        Markdown,
        NavLink,
        Outlet,
        Paragraph,
        Table,
        Text,
    ],
    Field(discriminator=COMPONENT_DISCRIMINATOR_NAME),
]


def ser_wrap(v, nxt: SerializerFunctionWrapHandler, info) -> dict:
    if getattr(v, COMPONENT_DISCRIMINATOR_NAME) == Custom.model_fields[COMPONENT_DISCRIMINATOR_NAME].default:
        return v.model_dump(by_alias=True)
    return nxt(v, info)


AnyComponent = Annotated[AnyComponentType, WrapSerializer(ser_wrap, when_used="json")]

# Rebuild forward ref models
for container_component in BaseContainerComponent.__subclasses__():
    container_component.model_rebuild()

__all__ = (
    "Avatar",
    "Button",
    "CodeBlock",
    "Container",
    "CopyButton",
    "Form",
    "Heading",
    "Link",
    "Markdown",
    "NavLink",
    "Outlet",
    "Paragraph",
    "Table",
    "Text",
    "AnyComponent",
)
