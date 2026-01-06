from fastapi import APIRouter

router = APIRouter(
    prefix="/healthz",
    tags=["healthz"],
)


@router.get("")
@router.get("/")
async def read_items():
    return {"status": "ok"}
