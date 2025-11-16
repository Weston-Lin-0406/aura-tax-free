from fastapi import APIRouter, File, UploadFile
from pyfk import CreateSuccessResponse

from library.seven_store_lib import SevenStoreLib

router = APIRouter(
    prefix="/data-import",
    tags=["data-import"]
)


@router.post("/seven-store", response_model=CreateSuccessResponse, description="7-11 門市匯入")
async def seven_store(file: UploadFile = File(...)):
    file.content_type
    await SevenStoreLib().import_store_by_pdf(file)
    return CreateSuccessResponse()