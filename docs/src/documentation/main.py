from flect import flect

from documentation import app as document_app

app = flect(document_app, docs_url="/documentation", debug=False)
