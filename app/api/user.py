from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.repository.user import create_new_user
from app.schemas.user import UserCreate, GetUser


api_router = APIRouter(prefix="", tags=["users"])


@api_router.post("/", response_model=GetUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    user = await create_new_user(user=user, db=db)
    return user
