from datetime import date, datetime, time
from pyfk import CrudSql
from sqlalchemy.orm.session import Session
from .schema import Orders
from typing import List

class OrdersDao(CrudSql[Orders]):

    def __init__(self, db: Session = None):
        super().__init__(db)

    def get_list_by_params(
            self,
            name: str,
            phone: str,
            store: str,
            is_export: bool,
            start_date:date,
            end_date: date) -> List[Orders]:
        
        query = self.db.query(Orders)

        if name:
            query = query.filter(Orders.name.like(f"%{name}%"))
        if phone:
            query = query.filter(Orders.phone.like(f"%{phone}%"))
        if store:
            query = query.filter(Orders.store_name.like(f"%{store}%"))
        if is_export == False:
            query = query.filter(Orders.is_export == is_export)
        if start_date:
            start_datetime = datetime.combine(start_date, time.min)
            query = query.filter(Orders.create_time >= start_datetime)
        if end_date:
            end_datetime = datetime.combine(end_date, time.max)
            query = query.filter(Orders.create_time <= end_datetime)

        return query.order_by(Orders.create_time.desc()).all()
    
    def get_list_by_uids(self, uids: List[str]) -> List[Orders]:
        """
        get orders by uid list
        """
        return self.db.query(Orders).filter(Orders.uid.in_(uids)).all()

    def get_last_order_by_user(self, user_id: str) -> Orders:
        """
        get last orders data by user id
        """
        return self.get_list(limit=1, order_by=(Orders.create_time.desc()), user_id=user_id)[0] or None