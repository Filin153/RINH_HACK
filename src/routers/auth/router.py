from src.models import User
from src.schemas import UserCreate, UserModel
import jwt
from .controllers import get_user, get_one_user, add_user, verify_user
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException, Request
from config import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/user",
    tags=["User"])


async def verify(request: Request, db: AsyncSession = Depends(get_async_session)):
    token = request.headers.get('token')
    if not token:
        raise HTTPException(status_code=401, detail="Требуется токен для доступа")

    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Не валидный токен")
    print(user_data)
    new_user = User(**user_data)

    if not await verify_user(db, user_data=new_user):
        await db.close()
        raise HTTPException(status_code=401, detail="Пароль")
    await db.close()

    return user_data


@router.get("/get", response_model=list[UserModel])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session),
                      user_data=Depends(verify)):
    users = await get_user(db, skip=skip, limit=limit)
    await db.close()
    return users


@router.get("/getone")
async def read_user(login, password: str, db: AsyncSession = Depends(get_async_session)):
    data_user = {"login": login, "password": password}
    new_user = User(**data_user)
    if not await verify_user(db, user_data=new_user):
        await db.close()
        raise HTTPException(status_code=401)
    user = await get_one_user(db, login=login)
    await db.close()
    if not user:
        raise HTTPException(status_code=400)
    json_data = {"login": user.login, "password": user.password, "id": user.id}
    return {"token": jwt.encode(json_data, SECRET_KEY, ALGORITHM)}


@router.post("/add")
async def add_users(user_data: UserCreate,
                     db: AsyncSession = Depends(get_async_session)):
    try:
        new_user = User(**user_data.dict())
        await add_user(db, user=new_user)
        await db.close()
        json_data = {"login": user_data.login, "password": user_data.password, "id": new_user.id}
        return {"token": jwt.encode(json_data, SECRET_KEY, ALGORITHM)}
    except Exception:
        raise HTTPException(status_code=409, detail="allready exists")
