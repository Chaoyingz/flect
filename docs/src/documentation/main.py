from flect import flect

from documentation import app as document_app
from documentation.config import settings

app = flect(
    document_app,
    docs_url="/documentation",
    debug=settings.debug,
    prebuilt_uri="/Users/chaoying/dev/os/flect/src/npm-flect-prebuilt/dist/assets",
)
