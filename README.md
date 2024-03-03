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

- The simple example shown below.

```python
from tui.response import PageResponse
from tui import components as c

async def page() -> PageResponse:
    return PageResponse(
        element=c.Text(
            text="Hello World!",
        )
    )
```

Which renders like this:
![tui-todo](https://github.com/Chaoyingz/tui/assets/32626585/f48415d8-b25c-432d-8dc4-d0bd4d65777d)

## Demo

Check out the `docs` folder in the project repository. The documentation website is built directly from these sources.

## License

This project is licensed under the terms of the MIT license.
