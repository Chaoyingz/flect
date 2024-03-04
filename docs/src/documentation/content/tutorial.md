# Tutorial

Welcome to the tutorial! We'll be building a small, but feature-rich todo app. We expect it to take around 30 minutes if you're following along.

## Setup

Before using this tutorial, we assume that you have already read the [Installation Guide](/docs/installation/) and have installed Rye and cookiecutter.

Create a new project using cookiecutter, as follows:

```console
cookiecutter https://github.com/Chaoyingz/cookiecutter-flect

# follow prompts
cd <your new project directory>
# install dependencies
rye sync
# run dev server
make dev
```

You should be able to visit the URL printed in the terminal:

```console
INFO:     Will watch for changes in these directories: ['/your/project/src']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [68051] using StatReload
INFO:     Started server process [68053]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then, open your browser and visit `http://127.0.0.1:8000`. You will see the following interface:

![welcome-to-flect](https://github.com/Chaoyingz/flect/assets/32626585/12c0f31b-8030-41b6-8c4b-3efb11e419ca)

## Modify Layout

A webpage is usually composed of a header, main, and footer. In the same website, most pages have the same header and footer, so there is no need to repeat these in every page. In flect, we can define a layout function, and all its subpages will automatically reuse this layout.

Edit `src/todo/app/layout.py`, as follows:

```python
from flect import PageResponse
from flect import components as c

async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Container(
                    tag="header",
                    class_name="h-14 border-b text-sm flex items-center px-6",
                    children=[
                        c.Link(
                            href="/",
                            children=[
                                c.Text(
                                    text="Todo",
                                    class_name="font-medium text-xl",
                                )
                            ],
                        ),
                    ]
                ),
                c.Container(
                    tag="main",
                    children=[outlet]
                ),
                c.Container(
                    tag="footer",
                    class_name="h-14 border-t text-sm flex items-center px-6",
                    children=[
                        c.Text(
                            text="Made with ❤️ by flect",
                        )
                    ],
                )
            ],
        )
    )
```

In the above code, we need to pay attention to a few details:

1. The layout is defined in the layout method in layout.py
2. The layout function must accept an `outlet` parameter, which will be the subpage
3. Each c.Container class will be rendered into the corresponding React component.
4. The function must return a page response

After modification, the page will automatically reload. If the modification is correct, you will see following:

![modify-layout](https://github.com/Chaoyingz/flect/assets/32626585/e3505877-e843-4d2c-bd0f-9c3c89bdaf2a)

You can see that the header and footer are reused in home page.
