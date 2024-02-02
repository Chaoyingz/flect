from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tui import init_tui
from tui.routing import get_router

from docs import app as docs_app

app = FastAPI()

tui_router = get_router(docs_app)
app.include_router(tui_router)
init_tui(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
