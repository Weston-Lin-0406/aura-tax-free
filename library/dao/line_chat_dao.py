from typing import List
from pyfk import CrudSql
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from .schema.customer import Customer
from .schema import LineChat

class LineChatDao(CrudSql[LineChat]):

    def __init__(self, db: Session = None):
        super().__init__(db)

    def get_user_not_download(self) -> List[str]:
        rows = self.db.query(LineChat.user_id) \
            .filter(LineChat.user_id.notin_(select(Customer.user_id))).all()
        return [r[0] for r in rows]