from fastapi import APIRouter, Depends, HTTPException
from .controllers import *
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.router import verify

router = APIRouter(
    tags=['VM'],
    prefix='/vm'
)


@router.get("/get/{servername}")
async def get_vm_conteiners(servername: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        await db.close()
        if get_linux_distribution(server.ip, server.user, server.password):
            res = get_running_vm_info_linux(server.ip, server.user, server.password)
        else:
            res = get_running_vm_info_windows(server.ip, server.user, server.password)
        return res
    except:
        raise HTTPException(status_code=400, detail="ВМ необнаруженно ")


@router.post("/stop/{id}")
async def stop_vm_conteiners(servername, vm_name: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        if get_linux_distribution(server.ip, server.user, server.password):
            res = stop_virtual_machine_linux(server.ip, server.user, server.password, vm_name)
        else:
            res = stop_virtual_machine_windows(server.ip, server.user, server.password, vm_name)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


@router.post("/start/{id}")
async def start_vm_conteiners(servername, vm_name: str, db: AsyncSession = Depends(get_async_session)):
    try:
        server = await get_one_server(db, servername)
        if get_linux_distribution(server.ip, server.user, server.password):
            res = start_virtual_machine_linux(server.ip, server.user, server.password, vm_name)
        else:
            res = start_virtual_machine_windows(server.ip, server.user, server.password, vm_name)
        return res
    except:
        raise HTTPException(status_code=400)
    finally:
        await db.close()


