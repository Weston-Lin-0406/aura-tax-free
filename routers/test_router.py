from fastapi import APIRouter

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

@router.get("/{name}")
async def index(name: str):
    return name