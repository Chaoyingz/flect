from tui import Response
from tui import components as c


async def page() -> Response:
    return Response(
        element=c.Container(
            tag="div",
            children=[
                c.Heading(
                    level=1,
                    text="Introduction",
                    class_name="text-3xl mb-3",
                ),
                c.Container(
                    class_name="mt-3",
                    children=[
                        c.Text(
                            text="Use Pydantic models in the backend that correspond to the properties of React components "
                            "in the frontend. This enables you to quickly develop interactive and beautiful UIs using "
                            "Python.",
                            class_name="text-md mt-3",
                        ),
                        c.Heading(text="The key features are:", level=2, class_name="mt-6 mb-3"),
                        c.Container(
                            class_name="flex flex-col gap-2",
                            children=[
                                c.Container(
                                    children=[
                                        c.Text(
                                            text="- Fast development: Write your entire app with Python, "
                                            "seamlessly integrating backend "
                                        ),
                                    ]
                                ),
                                c.Container(
                                    children=[
                                        c.Text(
                                            text="- SEO Friendly: Supports server-side rendering for better search engine visibility.",
                                        ),
                                    ]
                                ),
                                c.Container(
                                    children=[
                                        c.Text(
                                            text="- Client-Side Routing: Fast, smooth page transitions without reloads.",
                                        ),
                                    ]
                                ),
                                c.Container(
                                    children=[
                                        c.Text(
                                            text="- Folder-Based Routing: Easy route management through folder structure.",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        c.Container(class_name="mt-4", children=[c.Text(text="This project inspired by FastUI.")]),
                    ],
                ),
            ],
        )
    )
