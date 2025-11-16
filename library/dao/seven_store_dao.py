from pyfk import CrudSql
from sqlalchemy import delete
from sqlalchemy.orm.session import Session
from .schema import SevenStore

class SevenStoreDao(CrudSql[SevenStore]):

    def __init__(self, db: Session = None):
        super().__init__(db)

    def delete_all_store(self) -> int:
        result = self.db.execute(delete(self.table))
        self.commit()
        return result.rowcount