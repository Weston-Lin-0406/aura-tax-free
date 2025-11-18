from .orders_lib import OrdersLib
from .dao import LineChat, LineChatDao

class LineChatLib:

    dao: LineChatDao

    def __init__(self):
        self.dao = LineChatDao()

    def create(self, user_id: str, text: str) -> LineChat:
        # create line chat
        chat = LineChat(user_id, text)
        chat = LineChatDao().create(chat)
        # create order if text is order content
        OrdersLib().create_if_text_order_format(chat.uid, user_id, text)

        return chat