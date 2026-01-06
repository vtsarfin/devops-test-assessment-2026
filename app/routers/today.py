from fastapi import APIRouter, Depends
from datetime import date

from ..dependencies import get_query_token

router = APIRouter(
    prefix="/today",
    tags=["today"],
    dependencies=[Depends(get_query_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("")
@router.get("/")
async def read_items():
    return {"today": date.today()}
