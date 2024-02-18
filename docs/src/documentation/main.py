from tui import tui

from documentation import app as document_app

app = tui(document_app, docs_url="/documentation")
