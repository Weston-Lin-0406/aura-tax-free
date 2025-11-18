from pyfk import CrudSql
from sqlalchemy.orm.session import Session
from .schema import Orders

class OrdersDao(CrudSql[Orders]):

    def __init__(self, db: Session = None):
        super().__init__(db)

    def get_last_order_by_user(self, user_id: str) -> Orders:
        """
        get last orders data by user id
        """
        return self.get_list(limit=1, order_by=(Orders.create_time.desc()), user_id=user_id)[0] or None