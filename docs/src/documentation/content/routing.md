# Routing

Routing serves as the cornerstone of every application. This guide will delve into the crucial aspects of web routing and the best practices for managing routes in a Flex application.

## Route Segments

Route segments are represented by folders within a route, each corresponding to a specific segment of a URL path.

Consider this folder hierarchy:

```console
app
  ├── layout.py
  ├── page.py
  └── dashboard
      ├── page.py
      └── users
          └── page.py
```

In this layout, `dashboard` and `users` function as route segments. To access the `users` page within `dashboard`, the URL path would be `/dashboard/users`.

Each `page.py` file is associated with a distinct URL path, determined by its position in the directory structure:

- `app/page.py` corresponds to the root URL path (`/`), displaying the default page when visiting the application's base URL.
- `app/dashboard/page.py` is linked to `/dashboard/`, showing the relevant page upon navigation to this path.
- `app/dashboard/users/page.py` maps to `/dashboard/users/`, presenting the appropriate page for this path.

This setup allows each `page.py` file to represent a unique route, with the folder structure directly reflecting the routing architecture of the application. It simplifies the management and comprehension of your application's routes, making it intuitive and straightforward.

## Defining Routing Files

### layout.py

A layout defines a user interface (UI) shared across multiple routes, maintaining its state and interactivity across navigation without needing to re-render. Layouts can also be nested.

To define a layout:

```python
from flect import PageResponse
from flect import components as c

# The layout function should be named "layout" and take an "outlet" parameter
async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        body=c.Container(
            tag="div",
            class_name="flex",
            children=[outlet],  # the outlet renders the layout's content
        )
    )
```

### page.py

A page represents a UI specific to a route, with each distinct page corresponding to a separate `page.py` file.

To define a page:

```python
from flect import PageResponse
from flect import components as c

async def page() -> PageResponse:
    return PageResponse(
        body=c.Container(
            tag="div",
        )
    )
```

### routing.py

The `routing.py` file outlines your application's routes, often used for handling forms. For instance, you can define a POST endpoint to process form submissions as follows:

```python
from pydantic import BaseModel
from flect.actions import Notify
from flect.form import Input
from flect.response import ActionResponse

class FormExampleModel(BaseModel):
    username: str = Input(
        placeholder="Enter your username", default="", pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10
    )

async def post(form: FormExampleModel) -> ActionResponse:
    return ActionResponse(
        action=Notify(
            title=f"You submitted username: {form.username}",
        )
    )
```

Here, the route name corresponds to the method name, such as `post` for processing POST requests.

This approach offers a clear and scalable framework for managing your application's routing.
