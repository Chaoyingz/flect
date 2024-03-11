from typing import Literal, Optional, Union, cast

from pydantic import BaseModel, Field, field_validator


class TitleTemplate(BaseModel):
    template: Optional[str] = Field(default=None, description="The template of the title.")
    default: str = Field(..., description="The default title.")
    absolute: bool = Field(default=False, description="Determines if the title is absolute.")


class Meta(BaseModel):
    charset: Optional[str] = Field(default="utf-8", description="The charset of the page.")
    content: str = Field(..., description="The content of the page.")
    http_equiv: Optional[str] = Field(default=None, description="The httpEquiv of the page.", alias="http-equiv")
    name: str = Field(..., description="The name of the page.")

    def render_to_html(self) -> str:
        html = ""
        if self.http_equiv:
            html += f'<meta http-equiv="{self.http_equiv}" content="{self.content}">'
        else:
            html += f'<meta name="{self.name}" content="{self.content}">'
        return html


class HeadMetas(BaseModel):
    metas: list[Union[Meta, str]] = Field(default_factory=list, description="The metadata of the page.")
    absolute: bool = Field(default=False, description="Determines if the title is absolute.")


class HeadScript(BaseModel):
    cross_origin: Optional[Literal["anonymous", "use-credentials"]] = Field(
        default=None,
        description="Sets the mode of the request to an HTTP CORS Request.",
        alias="crossorigin",
    )
    defer: Optional[bool] = Field(
        default=None, description="Specifies that the script is executed when the page loads."
    )
    integrity: Optional[str] = Field(default=None, description="Specifies the cryptographic hash for the script.")
    no_module: Optional[bool] = Field(
        default=None,
        description="Specifies that the script is not a module script.",
        alias="nomodule",
    )
    referrer_policy: Optional[
        Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ]
    ] = Field(
        default=None,
        description="Specifies which referrer is sent when fetching the script.",
        alias="referrerpolicy",
    )
    src: str = Field(..., description="Specifies the URL of the script.")
    type: Optional[str] = Field(default=None, description="Specifies the type of the script.")

    def render_to_html(self) -> str:
        html = ""
        if self.cross_origin is not None:
            html += f'crossorigin="{self.cross_origin}" '
        if self.defer is not None:
            html += f'defer="{self.defer}" '
        if self.integrity is not None:
            html += f'integrity="{self.integrity}" '
        if self.no_module is not None:
            html += f'nomodule="{self.no_module}" '
        if self.referrer_policy is not None:
            html += f'referrerpolicy="{self.referrer_policy}" '
        if self.src is not None:
            html += f'src="{self.src}" '
        if self.type is not None:
            html += f'type="{self.type}" '
        return html


class HeadScripts(BaseModel):
    scripts: list[Union[HeadScript, str]] = Field(default_factory=list, description="The scripts of the page.")
    absolute: bool = Field(default=False, description="Determines if the scripts are absolute.")


class HeadLink(BaseModel):
    cross_origin: Optional[Literal["anonymous", "use-credentials"]] = Field(
        default=None,
        description="Sets the mode of the request to an HTTP CORS Request.",
        alias="crossorigin",
    )
    href: str = Field(..., description="Specifies the URL of the link.")
    hreflang: Optional[str] = Field(
        default=None,
        description="Specifies the language of the linked document.",
    )
    media: Optional[str] = Field(
        default=None, description="Specifies a hint of the media for which the linked document is displayed."
    )
    referrer_policy: Optional[
        Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ]
    ] = Field(
        default=None,
        description="Specifies which referrer is sent when fetching the script.",
        alias="referrerpolicy",
    )
    rel: Optional[
        Literal[
            "alternate",
            "author",
            "bookmark",
            "help",
            "icon",
            "license",
            "manifest",
            "next",
            "pingback",
            "prefetch",
            "prev",
            "search",
            "stylesheet",
        ]
    ] = Field(
        default=None,
        description="Specifies the relationship between the linked document and the current document.",
    )
    sizes: Optional[str] = Field(default=None, description="Specifies the sizes of the linked image.")
    title: Optional[str] = Field(default=None, description="Specifies the title of the link.")
    type: Optional[str] = Field(default=None, description="Specifies the type of the link.")

    def render_to_html(self) -> str:
        html = ""
        if self.cross_origin is not None:
            html += f'crossorigin="{self.cross_origin}" '
        if self.hreflang is not None:
            html += f'hreflang="{self.hreflang}" '
        if self.media is not None:
            html += f'media="{self.media}" '
        if self.referrer_policy is not None:
            html += f'referrerpolicy="{self.referrer_policy}" '
        if self.rel is not None:
            html += f'rel="{self.rel}" '
        if self.sizes is not None:
            html += f'sizes="{self.sizes}" '
        if self.title is not None:
            html += f'title="{self.title}" '
        if self.type is not None:
            html += f'type="{self.type}" '
        return html


class HeadLinks(BaseModel):
    links: list[Union[HeadLink, str]]
    absolute: bool = Field(default=False, description="Determines if the links are absolute.")


class Head(BaseModel):
    title: Union[str, TitleTemplate, None] = Field(default=None, description="The document title.")
    description: Optional[str] = Field(default=None, description="Standard metadata names.")
    script: Optional[HeadScripts] = Field(default=None, description="The scripts of the document.")
    link: Optional[HeadLinks] = Field(default=None, description="The links of the document.")
    meta: Optional[HeadMetas] = Field(default=None, description="The metadata of the document.")

    @field_validator("title")
    def validate_title(cls, value: Union[str, TitleTemplate, None]) -> Union[TitleTemplate, None]:
        if isinstance(value, str):
            return TitleTemplate(template=None, default=value, absolute=False)
        return value

    def render_to_html(self) -> str:
        html = ""
        if self.title is not None:
            title = cast(TitleTemplate, self.title)
            html += f"<title>{title.default}</title>\n"
        if self.description is not None:
            html += f'<meta name="description" content="{self.description}">\n'
        if self.script is not None:
            for script in self.script.scripts:
                if isinstance(script, str):
                    html += script
                else:
                    html += f"<script {script.render_to_html()}/>\n"
        if self.link is not None:
            for link in self.link.links:
                if isinstance(link, str):
                    html += link
                else:
                    html += f"<link {link.render_to_html()}/>\n"
        if self.meta is not None:
            for meta in self.meta.metas:
                if isinstance(meta, str):
                    html += meta
                else:
                    html += f"<meta {meta.render_to_html()}/>\n"
        return html


def merge_parent_title(parent_title: Union[TitleTemplate, str, None], child_title: TitleTemplate) -> TitleTemplate:
    if parent_title is None or child_title.absolute:
        return child_title
    if isinstance(parent_title, str):
        parent_title_template = TitleTemplate(
            template=None,
            default=parent_title,
            absolute=False,
        )
    else:
        parent_title_template = parent_title

    if parent_title_template.template:
        child_title.default = parent_title_template.template.format(title=child_title.default)
    else:
        child_title.default = f"{child_title.default} - {parent_title_template.default}"

    child_title.absolute = parent_title_template.absolute

    return child_title


def merge_head(parent: Head, child: Head) -> Head:
    if child.title is not None:
        child_title = cast(TitleTemplate, child.title) if child.title else None
        if child_title and not child_title.absolute:
            parent.title = merge_parent_title(parent.title, child_title)
        else:
            parent.title = child.title
    if child.description is not None:
        parent.description = child.description
    if child.script is not None:
        if child.script.absolute:
            parent.script = child.script
        else:
            if parent.script is None:
                parent.script = child.script
            else:
                parent.script.scripts.extend(child.script.scripts)
    if child.link is not None:
        if child.link.absolute:
            parent.link = child.link
        else:
            if parent.link is None:
                parent.link = child.link
            else:
                parent.link.links.extend(child.link.links)
    if child.meta is not None:
        if child.meta.absolute:
            parent.meta = child.meta
        else:
            if parent.meta is None:
                parent.meta = child.meta
            else:
                parent.meta.metas.extend(child.meta.metas)
    return parent
