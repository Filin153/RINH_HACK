from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(db: AsyncSession, skip: int = 0, limit: int = 100):
    q = select(User).offset(skip).limit(limit)
    moders = await db.execute(q)
    return moders.scalars().all()

async def get_one_user(db: AsyncSession, login: str):
    q = select(User).where(User.login == login)
    user = await db.execute(q)
    return user.scalars().first()

async def add_user(db: AsyncSession,
                   user: User
                   ):
    user.password = pwd_context.hash(user.password)
    db.add(user)
    await db.commit()
    return True


async def verify_user(db: AsyncSession,
                       user_data: User
                    ):
    q = select(User).where(User.login == user_data.login)
    user = await db.execute(q)
    user = user.scalars().first()
    if not user:
        return False
    if user_data.password == user.password:
        return True
    if not pwd_context.verify(user_data.password, user.password):
        return False
    return True
