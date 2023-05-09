from fastapi import APIRouter

"""
    Use APIRouter to declare path ops
"""
router = APIRouter()


@router.get("/")
async def index() -> dict[str, str]:
    return {"message": "Polls Index"}
