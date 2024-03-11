from flect import PageResponse
from flect import components as c
from flect.head import Head, HeadScripts, TitleTemplate

from documentation.config import settings


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        head=Head(
            title=TitleTemplate(template="{title} - flect", default="flect"),
            script=HeadScripts(
                scripts=[
                    f"<script async src='https://www.googletagmanager.com/gtag/js?id={settings.google_measurement_id}'></script>",
                    f"""
                    <script>
                      window.dataLayer = window.dataLayer || [];
                      function gtag(){{dataLayer.push(arguments);}}
                      gtag('js', new Date());

                      gtag('config', '{settings.google_measurement_id}');
                    </script>
                    """,
                ]
            ),
        ),
        body=c.Container(
            tag="div",
            children=[
                c.Container(
                    tag="header",
                    class_name="h-14 border-b text-sm",
                    children=[
                        c.Container(
                            class_name="flex w-full justify-between container items-center h-full",
                            children=[
                                c.Container(
                                    tag="nav",
                                    class_name="flex items-center gap-6",
                                    children=[
                                        c.Link(
                                            href="/",
                                            underline="none",
                                            children=[
                                                c.Text(
                                                    text="flect",
                                                    class_name="font-medium text-xl",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/docs/introduction/",
                                            underline="none",
                                            children=[
                                                c.Text(
                                                    text="Docs",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/avatar/",
                                            underline="none",
                                            children=[
                                                c.Text(
                                                    text="Components",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                c.Container(
                                    tag="div",
                                    children=[
                                        c.Link(
                                            href="https://github.com/Chaoyingz/flect",
                                            target="_blank",
                                            underline="none",
                                            children=[
                                                c.Text(
                                                    text="GitHub",
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                c.Container(
                    tag="main",
                    class_name="container min-h-screen",
                    children=[outlet],
                ),
                c.Container(
                    tag="footer",
                    class_name="border-t text-sm container py-8 mt-8 flex",
                    children=[
                        c.Paragraph(
                            class_name="text-sm",
                            text="Built by [Chaoying](https://github.com/Chaoyingz). The source code is available on [GitHub](https://github.com/Chaoyingz/flect/tree/main/docs).",
                        ),
                    ],
                ),
            ],
        ),
    )
