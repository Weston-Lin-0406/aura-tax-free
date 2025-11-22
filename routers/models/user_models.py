from datetime import date
from typing import List
from pydantic import BaseModel
from pyfk import Gender, UserStatus, UserRole

class UserModel(BaseModel):

    # 信箱
    email: str
    
    # 姓名
    name: str

    # 性別
    gender: Gender

    # 聯絡電話
    phone: str

    # 生日
    birth: date


class UserInput(UserModel):

    # 密碼
    password: str


class UserCreateModel(UserInput):
    """
    透過後台建立使用者時用的 input
    """
    # 狀態
    status: UserStatus

    # 角色
    roles: List[UserRole]