import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tui.components import Avatar, Button, Container

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/')
async def api_root():
    return [
        Button(children='Hello Button!'),
        Avatar(fallback='Hello Avatar!'),
        Container(
            tag='section',
            className='flex',
            components=[Button(children='Hello Container!'), Avatar(fallback='Hello Container!')],
        ),
    ]


@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
