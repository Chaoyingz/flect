# Form

The flect framework allows you to create forms with ease.

## Defining Your Form Model

To define your form model, you can use Python's `Annotated` and `pydantic`'s `BaseModel` and `Field`. Here's an example:

```python
from pydantic import BaseModel
from flect.form import Input

class FormExampleModel(BaseModel):
    # Use Annotated to define the field
    name: str = Input(placeholder="Enter your username", pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10)
```

In this example, we define a `name` field with a placeholder text "Enter your username". The field accepts alphanumeric characters with a minimum length of 2 and a maximum length of 10.

## Using the Form Model

Once you've defined your form model, you can use it in your form like so:

```python
from flect import components as c
from flect import PageResponse

def page() -> PageResponse:
    return PageResponse(
        body=c.Container(
            tag="div",
            children=[
                c.Form(
                    model=FormExampleModel,
                    submit_url="/"
                )
            ]
        )
    )
```

In this example, we create a `PageResponse` that contains a `Container` with a single child, a `Form` that uses the `FormExampleModel` we defined earlier. The form's `submit_url` is set to the root ("/").

## Adding Server Logic

After defining the form and its model, you can add server logic to handle the form submission. Here's a simple example:

```python
from flect.response import ActionResponse

async def post(form: FormExampleModel) -> ActionResponse:
    # handle the form
```

In this function, we define an asynchronous function `post` that accepts a `FormExampleModel` instance and returns an `ActionResponse`. You can add your form handling logic within this function.
