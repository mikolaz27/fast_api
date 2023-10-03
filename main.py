from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.views import router
from database_handler import database, engine, metadata

metadata.create_all(engine)

app = FastAPI()

origin = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origin=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# @app.get('/api')
# async def index_async():
#     return {"Hello": "Hello from async view"}
#
#
# @app.get('/')
# def index():
#     return {"Hello": "Hello from fastapi!!!"}

app.include_router(router, prefix="/posts", tags=["posts"])
