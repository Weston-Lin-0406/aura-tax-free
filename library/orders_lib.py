import io
import re

from routers.models.orders_models import OrdersCreateModel, OrdersUpdateModel
from .dao import Orders, OrdersDao

from typing import List
from openpyxl import load_workbook

class OrdersLib:

    dao: OrdersDao

    def __init__(self):
        self.dao = OrdersDao()
    
    def create(self,
            order: Orders = None,
            order_model: OrdersCreateModel = None,
            current_user: str = "system") -> Orders:
        if order:
            return self.dao.create(order)
        
        order = Orders(None, None, order_model.name, order_model.phone,
            order_model.email, order_model.store_code, order_model.store_name, current_user)
        
        return self.dao.create(order)
    
    def create_if_text_order_format(self, chat_uid: str, user_id: str, text: str):
        if self.is_text_order_content(text):
            # create order
            order = self.parse_text_to_order(chat_uid, user_id, text)
            if order:
                self.create(order=order)
    
    def is_text_order_content(self, text: str) -> bool:
        required = ["姓名", "電話", "收件門市", "門市店號"]
        for r in required:
            if r not in text:
                return False
        return True

    def parse_text_to_order(self, chat_uid: str, user_id: str, text: str) -> Orders:
        lines = text.splitlines(keepends=False)
        name = phone = email = store_code = store_name = None
        keywords = {
            "姓名": name, "電話": phone, "收件門市": store_code, "門市店號": store_name, "信箱": email
        }
        keywords = ["姓名", "電話", "收件門市", "門市店號", "信箱"]
        pattern = r'[:：]'
        for line in lines:
            for key in keywords:

                if not line.startswith(key):
                    continue

                tmp = re.split(pattern, line)
                if len(tmp) <= 1:
                    continue
                
                if key == "姓名":
                    name = tmp[-1].strip()
                elif key == "電話":
                    phone = tmp[-1].strip()
                elif key == "門市店號":
                    store_code = tmp[-1].strip()
                elif key == "收件門市":
                    store_name = tmp[-1].strip()
                elif key == "信箱":
                    email = tmp[-1].strip()
        
        if not name or not phone:
            return None

        return Orders(chat_uid, user_id, name, phone, email, store_code, store_name)
    
    def update(self, uid: str, source: OrdersUpdateModel, current_user: str) -> Orders:
        target = self.dao.merge_to_target(uid, source)
        return self.dao.update(target, current_user)
    
    def export_by_uids(self, uids: List[str]) -> io.BytesIO:
        orders_list = self.dao.get_list_by_uids(uids)

        wb = load_workbook("resources/711_shipment_import.xlsx")
        sheet = wb.active
        for idx, orders in enumerate(orders_list):
            sheet[f"B{idx + 4}"] = "張棋斐"
            sheet[f"C{idx + 4}"] = "0983160759"
            sheet[f"D{idx + 4}"] = "mithe9@gmail.com"
            sheet[f"E{idx + 4}"] = "1000"
            sheet[f"F{idx + 4}"] = orders.store_name
            sheet[f"G{idx + 4}"] = orders.store_code
            sheet[f"H{idx + 4}"] = orders.name
            sheet[f"I{idx + 4}"] = orders.phone
            sheet[f"J{idx + 4}"] = "mithe9@gmail.com"
        
        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        for orders in orders_list:
            orders.is_export = True
            self.dao.update(orders)

        return stream