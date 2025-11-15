from pyfk import CrudSql
from sqlalchemy.orm.session import Session
from .schema import Customner

class CustomnerDao(CrudSql[Customner]):

    def __init__(self, db: Session = None):
        super().__init__(db)