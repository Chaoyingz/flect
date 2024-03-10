from functools import lru_cache

from flect import PageResponse
from flect import components as c
from flect.head import Head, TitleTemplate

docs_nav = [
    c.Container(
        tag="div",
        children=[
            c.Heading(
                level=2,
                text="Getting Started",
                class_name="mb-2",
            ),
            c.Container(
                tag="nav",
                class_name="flex flex-col gap-2",
                children=[
                    c.NavLink(
                        href="/docs/introduction/",
                        children=[c.Text(text="Introduction", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/docs/installation/",
                        children=[c.Text(text="Installation", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/docs/tutorial/",
                        children=[c.Text(text="Tutorial", class_name="text-sm")],
                    ),
                ],
            ),
        ],
    ),
    c.Container(
        tag="div",
        children=[
            c.Heading(
                level=2,
                text="Learn",
                class_name="mb-2",
            ),
            c.Container(
                tag="nav",
                class_name="flex flex-col gap-2",
                children=[
                    c.NavLink(
                        href="/learn/project-structure/",
                        children=[c.Text(text="Project Structure", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/learn/routing/",
                        children=[c.Text(text="Routing", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/learn/form/",
                        children=[c.Text(text="Form", class_name="text-sm")],
                    ),
                ],
            ),
        ],
    ),
    c.Container(
        tag="div",
        children=[
            c.Heading(
                level=2,
                text="Actions",
                class_name="mb-2",
            ),
            c.Container(
                tag="nav",
                class_name="flex flex-col gap-2",
                children=[
                    c.NavLink(
                        href="/actions/notify/",
                        children=[c.Text(text="Notify", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/actions/redirect/",
                        children=[c.Text(text="Redirect", class_name="text-sm")],
                    ),
                ],
            ),
        ],
    ),
    c.Container(
        tag="div",
        children=[
            c.Heading(
                level=2,
                text="Components",
                class_name="mb-2",
            ),
            c.Container(
                tag="nav",
                class_name="flex flex-col gap-2",
                children=[
                    c.NavLink(
                        href="/components/avatar/",
                        children=[c.Text(text="Avatar", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/button/",
                        children=[c.Text(text="Button", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/code-block/",
                        children=[c.Text(text="Code Block", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/container/",
                        children=[c.Text(text="Container", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/form/",
                        children=[c.Text(text="Form", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/heading/",
                        children=[c.Text(text="Heading", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/link/",
                        children=[c.Text(text="Link", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/markdown/",
                        children=[c.Text(text="Markdown", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/table/",
                        children=[c.Text(text="Table", class_name="text-sm")],
                    ),
                    c.NavLink(
                        href="/components/text/",
                        children=[c.Text(text="Text", class_name="text-sm")],
                    ),
                ],
            ),
        ],
    ),
]


@lru_cache
def get_docs_pager(current_link: str) -> c.AnyComponent:
    links_texts = [(link.href, link.children[0].text) for section in docs_nav for link in section.children[1].children]

    try:
        current_index = next(i for i, (link, _) in enumerate(links_texts) if link == current_link)
    except StopIteration:
        return c.Container()

    prev_link_text = links_texts[current_index - 1] if current_index > 0 else None
    next_link_text = links_texts[current_index + 1] if current_index < len(links_texts) - 1 else None

    return c.Container(
        tag="div",
        class_name="mt-10 flex justify-between",
        children=[
            c.Link(
                href=prev_link_text[0],
                children=[c.Button(children=[c.Text(text=f"< {prev_link_text[1]}")], variant="outline", size="sm")],
            )
            if prev_link_text
            else c.Container(),
            c.Link(
                href=next_link_text[0],
                children=[c.Button(children=[c.Text(text=f"{next_link_text[1]} >")], variant="outline", size="sm")],
            )
            if next_link_text
            else c.Container(),
        ],
    )


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        head=Head(
            title=TitleTemplate(template="{title} - flect documentation", default="flect documentation", absolute=True)
        ),
        element=c.Container(
            tag="div",
            class_name="flex",
            children=[
                c.Container(
                    tag="aside",
                    class_name="py-8 pr-6 flex flex-col gap-6 w-60",
                    children=docs_nav,
                ),
                c.Container(tag="section", class_name="py-8 flex-1", children=[outlet]),
            ],
        ),
    )
