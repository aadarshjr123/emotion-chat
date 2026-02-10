from fastapi import APIRouter
from app.core.metrics import get_metrics_response

router = APIRouter()


@router.get("/metrics")
async def metrics():
    return get_metrics_response()
