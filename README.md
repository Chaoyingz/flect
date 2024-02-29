<!-- PROJECT LOGO -->
<div align="center">

  <h3 align="center">tui framework</h3>

  <p align='center'>
    <em>Turning ideas into web app fast.</em>
  </p>
  <p align="center">
    <a href="https://github.com/Chaoyingz/tui/actions?query=workflow" target="_blank">
        <img src="https://github.com/Chaoyingz/tui/actions/workflows/test.yaml/badge.svg?event=push&branch=main" alt="Test">
    </a>
  </p>
  <p align="center">
    <a href="https://tui.celerforge.com/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Chaoyingz/tui/blob/main/README_CN.md">简体中文</a>
    ·
    <a href="https://github.com/Chaoyingz/tui/issues">Report Bug</a>
    ·
    <a href="https://github.com/Chaoyingz/tui/issues">Request Feature</a>
  </p>
</div>

<!-- WHAT IS TUI -->

## What is tui?

tui is a Python framework for building full-stack web applications. It constructs user interfaces by utilizing Pydantic
models in the backend that correspond to the properties of React components in the frontend. This integration enables
quick development of interactive and beautiful UIs using Python.

The key features are:

- **Fast development**: Write your entire app with Python, seamlessly integrating backend logic and frontend UI.
- **Easy Form Validation**: Define a single Pydantic model for seamless and consistent form validation across your app, enhancing development speed and reducing potential errors.
- **Client-Side Routing**: Fast, smooth page transitions without reloads.
- **Folder-Based Routing**: Easy route management through folder structure.
- **SEO Friendly**: Supports server-side rendering for better search engine visibility.

## Requirements

- Python 3.9+

## Installation

```console
$ pip install tuiframework

---> 100%
```

## Example

- The simple todo app is shown below.

```python
import json
from typing import Annotated, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tui import PageResponse
from tui import components as c
from tui import form as f
from tui.actions import Notify
from tui.response import ActionResponse

# Define a model for creating new todo items with a single 'task' field
class TodoInCreate(BaseModel):
    task: Annotated[str, f.Input(placeholder="Enter task...")]

# Define a model for todo items stored in the database, extending the creation model with an 'id' and 'completed' field
class TodoInDB(TodoInCreate):
    id: int
    completed: Optional[bool] = False

# Initialize a list of todo items
todos = [
    TodoInDB(id=1, task="Task 1", completed=False),
    TodoInDB(id=2, task="Task 2", completed=True),
    TodoInDB(id=3, task="Task 3", completed=False),
]

# Define the page
async def page() -> PageResponse:
    return PageResponse(
        element=c.Container(
            # support tailwind css
            class_name="container mx-auto px-32 py-10",
            children=[
                # Add a heading to the page
                c.Heading(
                    level=1,
                    text="Todo App",
                    class_name="text-3xl mb-10",
                ),
                # Add a form for creating new todo items
                c.Form(
                    model=TodoInCreate,
                    submit_url="/",
                    class_name="mb-5 border p-5",
                ),
                # Add a table displaying all todo items
                c.Table(
                    datasets=todos,
                    class_name="border p-5",
                )
            ]
        )
    )

# Define the form handling logic
async def post(form: TodoInCreate) -> ActionResponse:
    todos.append(
        TodoInDB(
            id=len(todos) + 1,
            task=form.task,
            completed=False,
        )
    )
    # Return a notification with the submitted form values
    return ActionResponse(
        action=Notify(
            title="You submitted the following values:",
            description=json.dumps(jsonable_encoder(form), indent=2),
        )
    )
```

Which renders like this:
![tui-todo](https://github.com/Chaoyingz/tui/assets/32626585/f48415d8-b25c-432d-8dc4-d0bd4d65777d)

## Demo

Check out the `docs` folder in the project repository. The documentation website is built directly from these sources.

## License

This project is licensed under the terms of the MIT license.
