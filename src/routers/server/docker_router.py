from fastapi import APIRouter, Depends, HTTPException
from .controllers import *
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.router import verify

router = APIRouter(
    tags=['Docker'],
    prefix='/docker'
)


@router.get("/get/{servername}")
async def get_docker_conteiners(servername: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        await db.close()
        res = get_docker_containers(server.ip, server.user, server.password)
        return res
    except:
        raise HTTPException(status_code=400)


@router.post("/stop/{id}")
async def stop_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = stop_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/start/{id}")
async def start_docker_conteiners(servername, id: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = start_docker_container(server.ip, server.user, server.password, id)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/run")
async def run_docker_conteiners(servername, container_name, img: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = run_docker_container(server.ip, server.user, server.password, container_name, img)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.delete("/remove")
async def remove_docker_conteiners(servername, container: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = remove_docker_container(server.ip, server.user, server.password, container)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/pull")
async def pull_docker_conteiners(servername, name: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        res = pull_docker_container(server.ip, server.user, server.password, name)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


