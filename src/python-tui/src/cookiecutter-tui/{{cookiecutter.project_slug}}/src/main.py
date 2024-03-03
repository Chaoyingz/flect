from tui import tui

from {{cookiecutter.project_slug}} import app as {{cookiecutter.project_slug}}_app

app = tui({{cookiecutter.project_slug}}_app, docs_url="/documentation")
