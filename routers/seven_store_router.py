from fastapi import APIRouter, Depends, HTTPException, Path
from pyfk import BaseResponse, UserRole, authorization

from library.dao import SevenStoreDao
from .models.orders_models import *

router = APIRouter(
    prefix="/seven-store",
    tags=["seven-orders"]
)

@router.get("/name/{store_code}", response_model=BaseResponse[str], description="用7-11店號查門市名稱")
async def get_name_by_code(
        _: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        store_code: str = Path(...)):
    store = SevenStoreDao().get_one(code=store_code)
    if not store:
        raise HTTPException(status_code=404, detail="找不到該門市")
    
    return BaseResponse(data=store.name)

@router.get("/code/{store_name}", response_model=BaseResponse[str], description="用7-11門市名稱查店號")
async def get_code_by_name(
        _: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        store_name: str = Path(...)):
    store = SevenStoreDao().get_one(name=store_name.replace("門市", ""))
    if not store:
        raise HTTPException(status_code=404, detail="找不到該門市")
    
    return BaseResponse(data=store.code)