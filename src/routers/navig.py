from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.routers.server.controllers import get_all_user_server, get_docker_containers, make_docker_df, \
    get_running_vm_info_windows, get_running_vm_info_linux
import jwt
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException, Request
from config import SECRET_KEY, ALGORITHM

router = APIRouter(
    tags=['Navig'],
)

tmp = Jinja2Templates(directory="src/static")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return tmp.TemplateResponse("index.html", {"request": request})


@router.get("/main/{token}", response_class=HTMLResponse)
async def index(token: str, request: Request, db: AsyncSession = Depends(get_async_session)):
    print(token)
    user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    cont = await get_all_user_server(db, user_data['id'])
    docker_data = []
    win_data = []
    linux_data = []
    for i in cont:
        try:
            docker_data.append({"server": i.name, "data": get_docker_containers(i.ip, i.user, i.password)})
        except:
            pass
        try:
            win_data.append({"server": i.name, "data": get_running_vm_info_windows(i.ip, i.user, i.password)})
        except:
            pass
        try:
            linux_data.append({"server": i.name, "data": get_running_vm_info_linux(i.ip, i.user, i.password)})
        except:
            pass

    context = {"request": request, "username": user_data['login'],
               "docker_data": docker_data,
               "win_data": win_data,
               "linux_data": linux_data}
    return tmp.TemplateResponse("main.html", context)
