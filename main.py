from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src import auth_router, navig_router, server_router, docker_router, vm_router

app = FastAPI()


app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router)
app.include_router(navig_router)
app.include_router(server_router)
app.include_router(docker_router)
app.include_router(vm_router)