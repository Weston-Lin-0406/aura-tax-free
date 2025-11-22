from fastapi import APIRouter, Body, Depends
from pyfk import CreateSuccessResponse, authorization
from library.user_lib import UserLib
from .models.user_models import *

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/", response_model=CreateSuccessResponse, description="使用者新增")
async def create_user(
        current_user: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        user_form: UserCreateModel = Body(...)):
    UserLib().create(user_form, current_user)
    return CreateSuccessResponse()