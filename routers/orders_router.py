import csv
from datetime import date
import io
from typing import List
from fastapi import APIRouter, Body, Depends, Path, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pyfk import BaseResponse, CreateSuccessResponse, UserRole, authorization

from library.dao import OrdersDao
from library.orders_lib import OrdersLib
from .models.orders_models import *

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

template = Jinja2Templates(directory="resources/frontend")

@router.get("/index", response_class=HTMLResponse, description="訂單頁面")
async def index(request: Request):
    return template.TemplateResponse(request, "orders.html")

@router.get("/", response_model=BaseResponse[List[OrdersResponseModel]], description="取得訂單清單")
async def get_orders(
        _: str = Depends(authorization.verify()),
        name: Optional[str] = Query(None),
        phone: Optional[str] = Query(None),
        store: Optional[str] = Query(None),
        is_export: bool = Query(...),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None)):
    datas = OrdersDao().get_list_by_params(name, phone, store, is_export, start_date, end_date)
    return BaseResponse(data=OrdersResponseModel.init_list(datas))

@router.post("/", response_model=CreateSuccessResponse, description="新增訂單")
async def create_orders(
        current_user: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        orders: OrdersCreateModel = Body(...)):
    OrdersLib().create(order_model=orders, current_user=current_user)
    return CreateSuccessResponse()

@router.put("/{uid}", response_model=CreateSuccessResponse, description="更新訂單")
async def put_orders(
        current_user: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        uid: str = Path(...),
        orders: OrdersUpdateModel = Body(...)):
    OrdersLib().update(uid, orders, current_user)
    return CreateSuccessResponse()

@router.get("/export", description="匯出訂單")
async def export_orders(
        _: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        uids: List[str] = Query(...)):
    stream = OrdersLib().export_by_uids(uids)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=711_shipment_orders.xlsx"
        }
    )