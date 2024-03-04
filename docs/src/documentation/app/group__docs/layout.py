from flect import Meta, PageResponse, TitleTemplate
from flect import components as c


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        meta=Meta(title=TitleTemplate(template="{title} - flect", default="flect documentation", absolute=True)),
        element=c.Container(
            tag="div",
            class_name="flex",
            children=[
                c.Container(
                    tag="aside",
                    class_name="py-8 pr-6 flex flex-col gap-6 w-60",
                    children=[
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
                                            href="/docs/project-structure/",
                                            children=[c.Text(text="Project Structure", class_name="text-sm")],
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
                    ],
                ),
                c.Container(tag="section", class_name="py-8 flex-1", children=[outlet]),
            ],
        ),
    )
