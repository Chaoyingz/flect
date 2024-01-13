from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from tui.components import Avatar, Button, Container, Logo
from tui.prebuild import get_prebuild_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/')
async def home():
    return [
        Logo(text='tui', size='lg'),
        Button(children='Hello Button!'),
        Avatar(fallback='Hello Avatar!'),
        Container(
            tag='section',
            className='flex',
            components=[Button(children='Hello Container!'), Avatar(fallback='Hello Container!')],
        ),
    ]


@app.get('/')
async def prebuild():
    return HTMLResponse(get_prebuild_html('tui', 'https://cdn.jsdelivr.net/npm/@chaoying/npm-tui@0.1.0/dist'))
