from html import escape
from typing import Annotated, Literal, Optional, Union

import pyromark
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, SerializeAsAny, field_serializer, model_validator
from pydantic.alias_generators import to_camel
from typing_extensions import Self


class BaseComponent(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=AliasGenerator(serialization_alias=to_camel))

    class_name: Optional[str] = Field(
        None,
        description="Specifies the Tailwind CSS classes for the component.",
    )

    def render_to_html(self) -> str:
        return ""


class BaseContainerComponent(BaseComponent):
    children: Optional[list["AnyComponent"]] = Field(
        None,
        description="Defines the child components.",
    )


class Avatar(BaseComponent):
    component_type: Literal["avatar"] = "avatar"

    src: Optional[str] = Field(
        None,
        description="Specifies the image source for the avatar.",
    )
    alt: Optional[str] = Field(
        None,
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


class Button(BaseComponent):
    component_type: Literal["button"] = "button"

    variant: Literal["default", "destructive", "outline", "secondary", "ghost", "link"] = Field(
        "default",
        description="Determines the button's style variant.",
    )
    size: Literal["default", "sm", "lg", "icon"] = Field(
        "default",
        description="Determines the button's size.",
    )
    children: str

    def render_to_html(self) -> str:
        return f"""\
        <button>
            {escape(self.children)}
        </button>
        """


class CodeBlock(BaseComponent):
    component_type: Literal["code-block"] = "code-block"
    text: str = Field(
        ...,
        description="Specifies the code text.",
    )
    language: Optional[str] = Field(
        None,
        description="Defines the programming language for syntax highlighting.",
    )
    code_style: Optional[str] = Field(
        None,
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
    component_type: Literal["container"] = "container"

    tag: Literal["div", "section", "header", "footer", "main", "nav", "aside"] = Field(
        "div",
        description="Specifies the HTML tag for the container.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <{self.tag}>
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </{self.tag}>
        """


class CopyButton(BaseComponent):
    component_type: Literal["copy-button"] = "copy-button"
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


class Form(BaseComponent):
    component_type: Literal["form"] = "form"
    model: type[BaseModel] = Field(
        ...,
        description="Defines the form's data model.",
    )
    submit_method: Literal["POST", "PUT", "PATCH"] = Field(
        "POST",
        description="Specifies the HTTP method for form submission.",
    )
    submit_url: str = Field(
        ...,
        description="Specifies the URL where the form will be submitted.",
    )

    @field_serializer("model")
    def serialize_model(self, model: type[BaseModel]) -> dict:
        return model.model_json_schema()


class Heading(BaseComponent):
    component_type: Literal["heading"] = "heading"

    level: Literal[1, 2, 3, 4, 5, 6] = Field(
        ...,
        description="Determines the heading's level (1-6).",
    )
    text: str = Field(
        ...,
        description="Specifies the heading's text.",
    )
    id: Optional[str] = Field(
        None,
        description="Specifies the heading's id.",
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
        description="Specifies the URL for the link.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <a href="{escape(self.href)}">
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </a>
        """


class Markdown(BaseComponent):
    component_type: Literal["markdown"] = "markdown"

    text: str = Field(
        ...,
        description="Specifies the markdown text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        {pyromark.markdown(self.text)}
        """


class NavLink(BaseContainerComponent):
    component_type: Literal["nav-link"] = "nav-link"

    href: str = Field(
        ...,
        description="Specifies the URL for the navigation link.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <a href="{escape(self.href)}">
            {"".join(component.render_to_html() for component in self.children) if self.children else ""}
        </a>
        """


class Outlet(BaseComponent):
    component_type: Literal["outlet"] = "outlet"


class Paragraph(BaseComponent):
    component_type: Literal["paragraph"] = "paragraph"

    text: str = Field(
        ...,
        description="Specifies the paragraph's text.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <p>
            {escape(self.text)}
        </p>
        """


class Table(BaseComponent):
    component_type: Literal["table"] = "table"

    labels: list[str] = Field(
        [],
        description="Defines the table's column labels. Defaults to the keys of the dataset.",
    )
    datasets: list[SerializeAsAny[BaseModel]] = Field(
        ...,
        description="Specifies the table's data.",
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
                {"".join(f"<tr>{''.join(f'<td>{escape(str(getattr(dataset, label)))}</td>' for label in self.labels)}</tr>" for dataset in self.datasets)}
            </tbody>
        </table>
        """


class Text(BaseComponent):
    component_type: Literal["text"] = "text"

    text: str = Field(
        ...,
        description="Specifies the text content.",
    )

    def render_to_html(self) -> str:
        return f"""\
        <p>{escape(self.text)}</p>
        """


AnyComponent = Annotated[
    Union[
        Avatar,
        Button,
        CodeBlock,
        Container,
        CopyButton,
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
    Field(discriminator="component_type"),
]

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
