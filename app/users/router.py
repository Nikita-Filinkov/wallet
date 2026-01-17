from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.service import UsersService
from app.users.shemas import SUserAuth, UserShortResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserShortResponse)
async def register_user(
    register_data: SUserAuth,
) -> UserShortResponse:
    existing_user = await UsersService.find_one_or_none(email=register_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(register_data.password)
    user = await UsersService.add(
        email=register_data.email, hashed_password=hashed_password
    )

    return UserShortResponse(id=user.id, email=user.email)


@router.post("/login")
async def loging_user(response: Response, user_date: SUserAuth) -> str:
    user = await auth_user(email=user_date.email, password=user_date.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("wallet_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response) -> dict[str, str]:
    response.delete_cookie("wallet_access_token")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserShortResponse)
async def read_users_me(
    current_user: Users = Depends(get_current_user),
) -> UserShortResponse:
    return UserShortResponse(id=current_user.id, email=current_user.email)
