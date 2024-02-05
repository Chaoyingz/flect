# tui

Turning ideas into web app fast.

Use Pydantic models in the backend that correspond to the properties of React components in the frontend. This enables you to develop visually appealing and interactive user interfaces using Python.

## Documentation

https://tui.celerforge.com/

## Example

Create a file main.py with:

```python
from fastapi import FastAPI
from tui import init_tui
from tui import components as c

app = FastAPI()

@app.get("/api/")
def index() -> c.AnyComponents:
    return [c.Button(children="Hello tui!")]

init_tui(app)
```

Then run `uvicorn main:app` in your terminal and visit http://127.0.0.1:8000/ in your browser.

You will see the following:

![image](https://github.com/Chaoyingz/tui/assets/32626585/66993eb2-54c6-42d8-9054-94f0ad1d3f74)
