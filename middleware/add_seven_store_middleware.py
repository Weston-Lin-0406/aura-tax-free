from fastapi import Request, Response
from pyfk import url_middleware, UrlMiddleware, override

from library.dao import SevenStore, SevenStoreDao
from library.orders_lib import OrdersCreateModel

@url_middleware(url="/orders/", method="post", is_async=True)
class AddSevenStoreMiddleware(UrlMiddleware):

    @override(UrlMiddleware)
    def action(self,
        request: Request,
        response: Response,
        path_param: dict,
        query_param: dict,
        request_body: dict) -> Response:

        model = OrdersCreateModel(**request_body)
        dao = SevenStoreDao()
        store = dao.get_one(code=model.store_code)
        if not store:
            store = SevenStore(model.store_code, model.store_name)
            dao.create(store)
        return response