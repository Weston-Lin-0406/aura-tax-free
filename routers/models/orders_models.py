from typing import Optional
from pydantic import BaseModel
from pyfk import AbstractModel, ModelInitialization

class OrdersModel(BaseModel):

    name: Optional[str]

    phone: Optional[str]

    email: Optional[str]

    store_code: Optional[str]

    store_name: Optional[str]

class OrdersCreateModel(OrdersModel):

    pass

class OrdersUpdateModel(OrdersModel):

    is_export: bool

class OrdersResponseModel(OrdersModel, AbstractModel, ModelInitialization):

    is_export: bool