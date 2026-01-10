from pyfk import AbstractTable
from sqlalchemy import *
from sqlalchemy.orm import relationship

class Orders(AbstractTable):
    """
    訂單
    """
    __tablename__ = "orders"

    chat_uid = Column(String(length=32), ForeignKey("line_chat.uid"), nullable=True)
    chat = relationship("LineChat")

    user_id = Column(String(length=50), nullable=True)

    name = Column(String(length=50), nullable=True)

    phone = Column(String(length=15), nullable=True)

    email = Column(String(length=50), nullable=True)

    store_code = Column(String(length=10), nullable=True)

    store_name = Column(String(length=32), nullable=True)

    purchase = Column(String(length=100), nullable=True)

    is_export = Column(Boolean, default=False)

    is_delete = Column(Boolean, default=False)

    def __init__(self, chat_uid: str, user_id: str, name: str,
            phone: str, email: str, store_code: str, store_name: str, lm_user="system"):
        super().__init__(lm_user)
        self.chat_uid = chat_uid
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.email = email
        self.store_code = store_code
        self.store_name = store_name