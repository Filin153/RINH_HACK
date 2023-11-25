from fastapi import APIRouter, Depends, HTTPException
from src.models import User
from src.schemas import UserCreate, UserModel
import jwt
from .controllers import get_user, get_one_user, add_user, verify_user
from src.models.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

secret_key = 'your_secret_key_here'

router = APIRouter(
    prefix="/user",
    tags=["User"])

@router.get("/get", response_model=list[UserModel])
async def read_moders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    users = await get_user(db, skip=skip, limit=limit)
    await db.close()
    return users

@router.get("/getone")
async def read_moder(login: str, db: AsyncSession = Depends(get_async_session)):
    user = await get_one_user(db, login=login)
    await db.close()
    return user

@router.post("/add")
async def add_moders(user_data: UserCreate,
                     db: AsyncSession = Depends(get_async_session)):
    try:
        new_user = User(**user_data.dict())
        await add_user(db, user=new_user)
        await db.close()
        json_data = {"login": user_data.login, "password": user_data.password, "id": new_user.id}
        return jwt.encode(json_data, secret_key, 'HS256')
    except Exception:
        raise HTTPException(status_code=409, detail="allready exists")

@router.post("/verify", response_model=UserCreate)
async def verify_moser(token: str,
                     db: AsyncSession = Depends(get_async_session)):
    user_data = jwt.decode(token, secret_key, algorithms=['HS256'])
    new_user = User(**user_data.dict())
    if not await verify_user(db, user_data=new_user):
        await db.close()
        raise HTTPException(status_code=401)
    await db.close()
    return user_data