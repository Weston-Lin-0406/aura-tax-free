from pyfk import AbstractTable
from sqlalchemy import *

class LineChat(AbstractTable):
    """
    Line 顧客訊息紀錄
    """

    __tablename__ = "line_chat"

    user_id = Column(String(length=50), nullable=False)

    text = Column(Text, nullable=False)

    def __init__(self, user_id: str, text: str, lm_user="system"):
        super().__init__(lm_user)
        self.user_id = user_id
        self.text = text