# Routing

Routing is the foundation of every application. This guide will introduce the essential concepts of web routing and how to effectively manage routing in a flect application.

## Route Segments

Each folder in a route represents a route segment. Each route segment corresponds to a specific segment in a URL path.

Consider the following folder structure:

```console
app
  ├── layout.py
  ├── page.py
  └── dashboard
    ├── page.py
    └── users
      └── page.py
```

In this structure, `dashboard` and `users` are route segments. The URL path to access the `users` page under `dashboard` would be `/dashboard/users`.

In this example, each `page.py` file maps to a specific URL path based on its location in the folder structure:

- `app/page.py` maps to the root URL path (`/`). This is the default page displayed when users visit the base URL of your application.
- `app/dashboard/page.py` maps to `/dashboard/`. This is the page displayed when users navigate to the `/dashboard/` path in your application.
- `app/dashboard/users/page.py` maps to `/dashboard/users/`. This is the page displayed when users navigate to the `/dashboard/users/` path in your application.

This way, each `page.py` file serves as a unique route in your application, and the folder structure directly translates to the application's routing structure. This makes managing and understanding your application's routes straightforward and intuitive.

## Defining Routing Files

### layout.py

A layout is a user interface (UI) that is shared across multiple routes. Layouts maintain their state and remain interactive during navigation, without re-rendering. Layouts can also be nested.

Here's how you can define a layout:

```python
from flect import PageResponse
from flect import components as c

# The layout function must be named "layout" and accept an "outlet" parameter
async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        body=c.Container(
            tag="div",
            class_name="flex",
            # use the outlet to render the layout's content
            children=[outlet],
        )
    )
```

### page.py

A page is a UI that is unique to a specific route. Each unique page in the application corresponds to a `page.py` file.

Here's how you can define a page:

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

This structure provides a clear and scalable way to manage your application's routes.
