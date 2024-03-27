from flect import flect

from documentation import app as document_app
from documentation.config import settings

# PREBUILT_URI = str(pathlib.Path(__file__).parent.parent.parent / "docs-ui" / "dist" / "assets")
PREBUILT_URI = "https://unpkg.com/docs-ui@0.1.8/dist/assets"


app = flect(
    document_app,
    docs_url="/documentation",
    debug=settings.debug,
    prebuilt_uri=PREBUILT_URI,
)
