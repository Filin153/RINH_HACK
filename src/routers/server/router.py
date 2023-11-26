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
        cont = get_docker_containers(server.ip, server.user, server.password)
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


