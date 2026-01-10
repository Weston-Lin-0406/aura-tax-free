from pyfk import AbstractTable
from sqlalchemy import *

class SevenStore(AbstractTable):
    """
    7-11 門市資料
    """

    __tablename__ = "seven_store"

    code = Column(String(length=10), nullable=False)

    name = Column(String(length=32), nullable=False)

    city = Column(String(length=32), nullable=True)

    address = Column(String(length=50), nullable=True)

    phone_code = Column(String(length=3), nullable=True)

    phone_number = Column(String(length=10), nullable=True)

    def __init__(
            self,
            code: str,
            name: str,
            city: str = None,
            address: str = None,
            phone_code: str = None,
            phone_number: str = None,
            lm_user="system"):
        super().__init__(lm_user)
        self.code = code
        self.name = name
        self.city = city
        self.address = address
        self.phone_code = phone_code
        self.phone_number = phone_number