from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import get_async_session
from src.routers.auth.router import verify
from src.routers.server.controllers import get_all_user_server, get_docker_containers, make_docker_df

router = APIRouter(
    tags=['Navig'],
)

tmp = Jinja2Templates(directory="src/static")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return tmp.TemplateResponse("index.html", {"request": request})

@router.get("/main", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_async_session)):
    cont = await get_all_user_server(db, 17)
    docker_data = []
    for i in cont:
        docker_data.append({"server": i.name, "data": get_docker_containers(i.ip, i.user, i.password)})
    print(docker_data)
    context = {"request": request, "username": "user_data['login']", "docker_data": docker_data}
    return tmp.TemplateResponse("main.html", context)