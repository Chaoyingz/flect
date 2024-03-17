from flect import flect

from documentation import app as document_app
from documentation.config import settings

app = flect(
    document_app,
    docs_url="/documentation",
    debug=settings.debug,
    prebuilt_uri="https://unpkg.com/docs-ui@0.1.6/dist/assets",
)
