<!-- PROJECT LOGO -->
<div align="center">

  <h3 align="center">flect</h3>

  <p align='center'>
    <em>Turning ideas into web app fast.</em>
  </p>
  <p align="center">
    <a href="https://github.com/Chaoyingz/flect/actions?query=workflow" target="_blank">
        <img src="https://github.com/Chaoyingz/flect/actions/workflows/test.yaml/badge.svg?event=push&branch=main" alt="Test">
    </a>
    <a href="https://pypi.python.org/pypi/flect" target="_blank">
        <img src="https://img.shields.io/pypi/v/flect.svg" alt="pypi">
    </a>
    <a href="https://github.com/Chaoyingz/flect" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/flect.svg" alt="versions">
    </a>
    <a href="https://github.com/Chaoyingz/flect/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/github/license/chaoyingz/flect.svg" alt="license">
    </a>
  </p>
  <p align="center">
    <a href="https://flect.celerforge.com/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Chaoyingz/flect/issues">Report Bug</a>
    ·
    <a href="https://github.com/Chaoyingz/flect/issues">Request Feature</a>
    ·
    <a href="https://github.com/Chaoyingz/flect/blob/main/README_CN.md">简体中文</a>
  </p>
</div>

<!-- WHAT IS flect -->

## What is flect?

flect is a Python framework for building full-stack web applications. It constructs user interfaces by utilizing Pydantic
models in the backend that correspond to the properties of React components in the frontend. This integration enables
quick development of interactive and beautiful UIs using Python.

The key features are:

- **Fast development**: Write your entire app with Python, seamlessly integrating backend logic and frontend UI.
- **Easy Form Validation**: Define a single Pydantic model for seamless and consistent form validation across your app, enhancing development speed and reducing potential errors.
- **Folder-Based Routing**: Easy route management through folder structure.
- **Client-Side Routing**: Fast, smooth page transitions without reloads.
- **SEO Friendly**: Supports server-side rendering for better search engine visibility.
- **Custom Components**: You can conveniently use your own built React components in flect.

You can also view the [documentation website](https://flect.celerforge.com/docs/introduction/), which is completely built with flect, source code can be found [here](https://github.com/Chaoyingz/flect/tree/main/docs).

## Why use flect?

flect enables developers to harness the combined power of Python and JavaScript ecosystems, facilitating the creation of web applications with efficiency and ease:

> If you're a Python developer — you can build responsive web applications using React without writing a single line of JavaScript, or touching npm.
>
> If you're a frontend developer — you can concentrate on building magical components that are truly reusable, no copy-pasting components for each view.
>
> For everyone — a true separation of concerns, the backend defines the entire application; while the frontend is free to implement just the user interface.
>
> — _From FastUI_

## Example

In this example, we will demonstrate how to build a simple to-do application using flect. As flect is built on top of [FastAPI](https://fastapi.tiangolo.com/), so you can define your routes using FastAPI’s syntax.

Note: In real-world flect applications, define page routes and post routes in separate files for better organization.

Below is a simple to-do application.

```python
import json
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from flect import PageResponse, ActionResponse
from flect import components as c
from flect import form as f
from flect.actions import Notify

# Define a model for creating new todo items with a single 'task' field
class TodoInCreate(BaseModel):
    task: str = f.Input(placeholder="Enter task...")

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
        body=c.Container(
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
                    model=TodoInDB
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
![flect-todo](https://github.com/Chaoyingz/flect/assets/32626585/f48415d8-b25c-432d-8dc4-d0bd4d65777d)

## Learn More

- [Documentation](https://flect.celerforge.com/)

## Credits

This project draws inspiration from the following frameworks:

- [FastUI](https://github.com/pydantic/FastUI)
- [Next.js](https://nextjs.org/)

## License

This project is licensed under the terms of the MIT license.
