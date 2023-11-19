from datetime import datetime
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import JWT_SECRET_KEY
from app.config import TOKEN_LIFESPAN
from app.config import VERIFY_SIGNATURE
from app.database import get_async_session
from app.models.user import User
from app.orm.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def create_access_token(user: User):
    token_exp_time = int(datetime.now().timestamp()) + TOKEN_LIFESPAN

    payload = {"username": user.username, "email": user.email, "exp": token_exp_time}

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=VERIFY_SIGNATURE)
    return token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[VERIFY_SIGNATURE])
        username = payload.get("username")

        if username is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature has expired",
        )

    except DecodeError:
        raise credentials_exception

    user = await get_user_by_username(db=db, username=username)
    if user is None:
        raise credentials_exception
    return user
