from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
import jwt
from passlib.context import CryptContext

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.schemas.auth_schemas import UserSchemaAdd

SECRET_KEY = "a9f3K2mX7vP1sQ8dL0zZ6xW4rT9uY5cN1bA7"
ALGORITHM = "HS256"

password_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def add_user(self, user: UserSchemaAdd):

        query = text("""
            INSERT INTO users (login, password_hash, role)
            VALUES (:login, :password_hash, :role)
            RETURNING id, login, role
        """)

        result = await self.session.execute(
            query,
            {
                "login": user.login,
                "password_hash": password_hashing.hash(user.password),
                "role": user.role
            }
        )

        await self.session.commit()

        return result.fetchone()

    async def authenticate(self, login: str, password: str):

        query = text("""
            SELECT id, login, password_hash, role
            FROM users
            WHERE login = :login
        """)

        result = await self.session.execute(
            query,
            {"login": login}
        )

        user = result.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password"
            )

        if not password_hashing.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password"
            )

        return {
            "id": user.id,
            "login": user.login,
            "role": user.role
        }

    @staticmethod
    def create_access_token(
        username: str,
        user_id: int,
        expires_delta: timedelta
    ):

        encode = {
            "sub": username,
            "id": user_id
        }

        expires = datetime.utcnow() + expires_delta

        encode.update({
            "exp": expires
        })

        return jwt.encode(
            encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def get_current_user(token: str):

        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        try:
            token = token.strip()
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            username = payload.get("sub")
            user_id = payload.get("id")

            return {
                "user_id": user_id,
                "username": username
            }

        except jwt.ExpiredSignatureError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        except jwt.InvalidTokenError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:  # на время отладки
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token error: {str(e)}"
            )
