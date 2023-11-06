from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas.user import UserCreate
from app.service.hashing import Hasher


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.first()


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.first()


async def create_new_user(user: UserCreate, db: AsyncSession):
    query = insert(User).values(
        username=user.username,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False
    ).returning(User)

    result = await db.execute(query)
    created_user = result.scalar()
    await db.commit()
    return created_user
