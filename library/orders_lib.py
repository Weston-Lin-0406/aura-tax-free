import re
from .dao import Orders, OrdersDao

class OrdersLib:

    dao: OrdersDao

    def __init__(self):
        self.dao = OrdersDao()
    
    def create(self,
            order: Orders = None,
            name: str = None,
            phone: str = None,
            email: str = None,
            store_code: str = None,
            store_name: str = None) -> Orders:
        if order:
            return self.dao.create(order)
        
        return Orders(None, None, name, phone, email, store_code, store_name)
    
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