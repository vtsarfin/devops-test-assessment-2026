from fastapi import APIRouter, Depends
from ..dependencies import get_query_token

version = "0.9"
router = APIRouter(
    prefix="/version",
    tags=["version"],
    dependencies=[Depends(get_query_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("")
@router.get("/")
async def read_items():
    return {"Version": version}
