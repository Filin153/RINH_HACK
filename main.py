from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src import auth_router, first_router, server_router

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")


app.include_router(auth_router)
app.include_router(first_router)
app.include_router(server_router)