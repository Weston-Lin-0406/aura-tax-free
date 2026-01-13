from fastapi import APIRouter, Depends, File, UploadFile
from pyfk import CreateSuccessResponse, UserRole, authorization

from library.seven_store_lib import SevenStoreLib

router = APIRouter(
    prefix="/data-import",
    tags=["data-import"]
)


@router.post("/seven-store", response_model=CreateSuccessResponse, description="7-11 門市匯入")
async def seven_store(
        current_user: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR)),
        file: UploadFile = File(...)):
    await SevenStoreLib().import_store_by_pdf(file, current_user)
    return CreateSuccessResponse()

@router.post("/seven-store/ibon", response_model=CreateSuccessResponse, description="7-11 門市匯入(ibon)")
async def seven_store_by_ibon(
        current_user: str = Depends(authorization.verify(UserRole.ADMIN, UserRole.OPERATOR))):
    await SevenStoreLib().import_store_by_ibon(current_user)
    return CreateSuccessResponse()