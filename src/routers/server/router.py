from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import ServerModel
from src.models import User
from src.schemas import UserCreate, UserModel, ServerModel, ServerCreate
from .controllers import *
from src.models.database import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    tags=['Server'],
    prefix='/server'
)


@router.post("/add/{login}")
async def add_server(login: str, server: ServerCreate, db: AsyncSession = Depends(get_async_session)):
    try:
        await create_user_server(db=db, server=server, login=login)
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()
    return get_docker_containers(server.ip, server.user, server.password).to_dict()


@router.get("/docker/get/{servername}")
async def get_docker_conteiners(servername: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        await db.close()
        res = get_docker_containers(server.ip, server.user, server.password)
        return res.to_dict()
    except:
        raise HTTPException(status_code=400)


@router.post("/docker/stop/{id}")
async def stop_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = stop_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/docker/start/{id}")
async def start_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = start_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/docker/run")
async def run_docker_conteiners(servername, container_name, img: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = run_docker_container(server.ip, server.user, server.password, container_name, img)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()

@router.delete("/docker/remove")
async def remove_docker_conteiners(servername, container: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = remove_docker_container(server.ip, server.user, server.password, container)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()

@router.post("/docker/pull")
async def pull_docker_conteiners(servername, name: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = pull_docker_container(server.ip, server.user, server.password, name)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()
