from pyfk import CrudSql
from sqlalchemy.orm.session import Session
from .schema import Customer

class CustomerDao(CrudSql[Customer]):

    def __init__(self, db: Session = None):
        super().__init__(db)