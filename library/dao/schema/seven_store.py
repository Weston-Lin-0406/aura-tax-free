from pyfk import AbstractTable
from sqlalchemy import *

class SevenStore(AbstractTable):
    """
    7-11 門市資料
    """

    __tablename__ = "seven_store"

    code = Column(String(length=10), nullable=False)

    name = Column(String(length=32), nullable=False)

    city = Column(String(length=32), nullable=False)

    address = Column(String(length=50), nullable=False)

    phone_code = Column(String(length=3), nullable=False)

    phone_number = Column(String(length=10), nullable=False)

    def __init__(self, code: str, name: str, city: str, address: str, phone_code: str, phone_number: str, lm_user="system"):
        super().__init__(lm_user)
        self.code = code
        self.name = name
        self.city = city
        self.address = address
        self.phone_code = phone_code
        self.phone_number = phone_number