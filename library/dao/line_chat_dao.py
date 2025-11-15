from pyfk import CrudSql
from sqlalchemy.orm.session import Session
from .schema import LineChat

class LineChatDao(CrudSql[LineChat]):

    def __init__(self, db: Session = None):
        super().__init__(db)