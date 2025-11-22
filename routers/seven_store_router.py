from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyfk import BaseResponse, UserRole, authorization

from library.dao import SevenStoreDao
from .models.orders_models import *

router = APIRouter(
    prefix="/seven-store",
    tags=["seven-orders"]
)

@router.get("/{store_code}", response_model=BaseResponse[str], description="用7-11店號查門市名稱")
async def get_by_code(
        _: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        store_code: str = Path(...)):
    store = SevenStoreDao().get_one(code=store_code)
    if not store:
        raise HTTPException(status_code=404, detail="找不到該門市")
    
    return BaseResponse(data=store.name)