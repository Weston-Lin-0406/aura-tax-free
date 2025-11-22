from pyfk import User, UserDao
from routers.models.user_models import *

from datetime import date

class UserLib:

    def __init__(self) -> None:
        self.dao = UserDao()

    def create_root_user(self) -> User:
        """
        create root user
        """
        user = User("aura@gmail.com", "auraroot", "闆闆", Gender.WOMAN, "09123456789", date.today())
        user.status = UserStatus.ENABLED
        user.set_roles(UserRole.ADMIN)
        return self.dao.create(user)

    def create(self, user_form: UserCreateModel, current_user: str) -> User:
        """
        create user

        args:
           user_form(UserCreateModel): create user input
           current_user(str): login user uid

        return:
            FaithtaxUser
        """
        user = User(user_form.email, user_form.password,
            user_form.name, user_form.gender, user_form.phone, user_form.birth)
        user.status = user_form.status
        user.set_roles(*user_form.roles)
        user.lm_user = current_user
        return self.dao.create(user)