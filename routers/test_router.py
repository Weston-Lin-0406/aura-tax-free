from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

@router.get("/index/{name}")
async def index(name: str):
    return name

@router.get("/scheduler/download-customer")
async def test_download_customer_scheduler():
    from scheduler.download_customer_scheduler import process
    process()