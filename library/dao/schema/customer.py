from pyfk import AbstractTable
from sqlalchemy import *


class Customner(AbstractTable):

    __tablename__ = "customer"

    user_id = Column(String(length=50), nullable=False)

    name = Column(String(length=50), nullable=False)

    avatar = Column(String(length=50), nullable=False)

    def __init__(self, user_id: str, name: str, avatar: str, lm_user="system"):
        super().__init__(lm_user)
        self.user_id = user_id
        self.name = name
        self.avatar = avatar