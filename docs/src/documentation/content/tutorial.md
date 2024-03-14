# Tutorial

Welcome to the tutorial! We'll be building a simple ToDo application. We expect it to take around 10 minutes if you're following along.

![todo](https://github.com/Chaoyingz/flect/assets/32626585/c66f67c7-4d0a-43a2-80ac-32eaecd3c802)

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
        body=c.Container(
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
                    class_name="p-12",
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

You can see that the header and footer are reused in the home page.

## Add ToDo Form

You may have noticed that after editing the layout, two headers appear on the page. This is because we have defined an additional header in the page. Next, we will write a ToDo form.

Edit the `src/todo/app/page.py` file and add the following code:

```python
from pydantic import BaseModel

from flect import PageResponse
from flect import components as c
from flect import form

class TodoInCreate(BaseModel):
    name: str = form.Input(placeholder="Enter task name...", max_length=16)

todos = {}

async def page() -> PageResponse:
    return PageResponse(
        body=c.Container(
            tag="section",
            children=[
                c.Form(
                    model=TodoInCreate,
                    submit_url="/",
                    class_name="mb-5 border p-5",
                )
            ],
        ),
    )
```

In the above code, we have defined a ToDo creation form using a pydantic model. Flect will automatically render this form. You will see the following page:

![add-todo-form](https://github.com/Chaoyingz/flect/assets/32626585/fccb63e2-9a7c-491f-bbf8-6d2eac671f7c)

Flect will parse the form validation items and add front-end validation.

## Handle Form

In the previous step, we defined a form. The form's submit_url provides the form submission address. Now we need to handle the submitted form data and save the data. In flect, you can define other methods under the current URL by creating a `route.py` file in the folder.

Edit the `src/todo/app/route.py` file and add the following code:

```python
from flect.actions import Notify
from flect.response import ActionResponse

from todo.app.page import TodoInCreate

async def post(form: TodoInCreate) -> ActionResponse:
    return ActionResponse(
        action=Notify(title="success", style="success", description=f"todo {form.name} created."),
    )
```

In the above code, we created a post interface to handle the add ToDo request and return a notification.

You will see the following page:
![handle-form](https://github.com/Chaoyingz/flect/assets/32626585/84675c6e-25cc-47d7-9913-9d9efd37ae44)

## Add Storage

We have defined a ToDo form, now we need to save the form data to the database.

For simplicity, we will use a json file to save the ToDo data.

Edit the `src/todo/storage.py` file and add the following code:

```python
import json
from pathlib import Path

class Storage:
    JSON_URI = Path(__file__).parent / "todos.json"

    def __init__(self) -> None:
        if not self.JSON_URI.exists():
            self.JSON_URI.touch(exist_ok=True)

    def insert(self, item: dict) -> None:
        with self.JSON_URI.open("a") as f:
            f.write(f"{json.dumps(item)}\n")

    def list(self) -> list[dict]:
        with self.JSON_URI.open("r") as f:
            return [json.loads(line) for line in f]

storage = Storage()
```

## Link Storage with Page

Display existing ToDos on the page:

Edit the `src/todo/app/page.py` file and add the following code:

```python
import uuid

from pydantic import BaseModel, Field

from flect import PageResponse
from flect import components as c
from flect import form

from todo.storage import storage

class TodoInCreate(BaseModel):
    name: str = form.Input(placeholder="Enter task name...", max_length=16)

class TodoInDB(TodoInCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

async def page() -> PageResponse:
    todos = [TodoInDB(**todo) for todo in storage.list()]
    return PageResponse(
        body=c.Container(
            tag="section",
            children=[
                c.Form(
                    model=TodoInCreate,
                    submit_url="/",
                    class_name="mb-5 border p-5",
                ),
                c.Table(
                    datasets=todos,
                )
            ],
        ),
    )
```

Edit the `src/todo/app/route.py` file and add the following code:

```python
from flect.actions import Notify
from flect.response import ActionResponse

from todo.app.page import TodoInCreate, TodoInDB
from todo.storage import storage

async def post(form: TodoInCreate) -> ActionResponse:
    storage.insert(TodoInDB(**form.dict()).model_dump())
    return ActionResponse(
        action=Notify(title="success", style="success", description=f"todo {form.name} created."),
    )
```

Now our ToDo application should work properly.

## Conclusion

Congratulations on completing this tutorial! You now have a working ToDo application built with the power of Flect. As you continue to explore Flect, remember that it can be used to build a wide variety of applications, not just ToDo lists.

In fact, this very documentation was written using Flect. You can refer to the [Flect Documentation Repository](https://github.com/Chaoyingz/flect/tree/main/docs) on GitHub to see how it was done.

Additionally, applications written with Flect can be directly deployed using Vercel, providing a seamless development to deployment experience. Happy coding!
