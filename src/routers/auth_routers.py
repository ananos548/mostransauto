from datetime import timedelta
from starlette import status
from fastapi import APIRouter, Depends, Cookie, Response, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.services.auth import AuthService
from src.schemas.auth_schemas import UserSchemaAdd


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],

)


@router.post("/registration")
async def create_user(
    new_user: UserSchemaAdd,
    service: AuthService = Depends(AuthService)
):

    user = await service.add_user(new_user)

    return {
        "user_id": user.id,
        "login": user.login
    }


@router.post("/login")
async def login_for_access_token(
    service: AuthService = Depends(AuthService),
    form_data: OAuth2PasswordRequestForm = Depends(),
    cookie_jwt: str = Cookie(default=None)
):

    if cookie_jwt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already authenticated"
        )

    user = await service.authenticate(
        form_data.username,
        form_data.password
    )

    token = service.create_access_token(
        user_id=user["id"],
        username=user["login"],
        expires_delta=timedelta(days=30)
    )

    response = JSONResponse(
        content={
            "message": "successfully"
        }
    )

    response.set_cookie(
        key="cookie_jwt",
        value=token,
        httponly=True
    )

    return response


@router.post("/logout")
async def logout(
    response: Response,
    cookie_jwt: str = Cookie(default=None, alias="cookie_jwt"),
    service: AuthService = Depends(AuthService)
):
    if not cookie_jwt:
        return {"message": "Already logged out"}  # не ошибка

    # Опционально: можно проверить токен перед удалением
    try:
        service.get_current_user(cookie_jwt)
    except HTTPException:
        pass  # даже если токен кривой — просто удаляем

    response.delete_cookie(
        key="cookie_jwt",
        httponly=True,
    )
    
    return {"message": "Logged out successfully"}

@router.get("/current_user")
async def get_current_user(
    cookie_jwt: str | None = Cookie(default=None),
    service: AuthService = Depends(AuthService)
):

    if not cookie_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_data = service.get_current_user(cookie_jwt)

    return user_data

