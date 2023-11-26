from fastapi import APIRouter, Depends, HTTPException
from .controllers import *
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.router import verify

router = APIRouter(
    tags=['Server'],
    prefix='/server'
)


@router.post("/add")
async def add_server(server: ServerCreate, db: AsyncSession = Depends(get_async_session),
                     user_data=Depends(verify)):
    try:
        cont = get_docker_containers(server.ip, server.user, server.password).to_dict()
        if cont:
            await create_user_server(db=db, server=server, login=user_data['login'])
    except:
        raise HTTPException(status_code=400, detail="Сервер с таким именем уже существует")
    finally:
        await db.close()
    return cont

@router.get("/get")
async def add_server(db: AsyncSession = Depends(get_async_session),
                     user_data=Depends(verify)):
    try:
        cont = await get_all_user_server(db, user_data['id'])
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()
    return cont


@router.get("/docker/get/{servername}")
async def get_docker_conteiners(servername: str, db: AsyncSession = Depends(get_async_session),
                                user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        await db.close()
        res = get_docker_containers(server.ip, server.user, server.password)
        return res.to_dict()
    except:
        raise HTTPException(status_code=400)


@router.post("/docker/stop/{id}")
async def stop_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session),
                                 user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        res = stop_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/docker/start/{id}")
async def start_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session),
                                  user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        res = start_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/docker/run")
async def run_docker_conteiners(servername, container_name, img: str, db: AsyncSession = Depends(get_async_session),
                                user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        res = run_docker_container(server.ip, server.user, server.password, container_name, img)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.delete("/docker/remove")
async def remove_docker_conteiners(servername, container: str, db: AsyncSession = Depends(get_async_session),
                                   user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        res = remove_docker_container(server.ip, server.user, server.password, container)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/docker/pull")
async def pull_docker_conteiners(servername, name: str, db: AsyncSession = Depends(get_async_session),
                                 user_data=Depends(verify)):
    try:
        server = await get_one_server(db, servername)
        res = pull_docker_container(server.ip, server.user, server.password, name)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()
