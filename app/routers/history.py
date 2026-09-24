from collections import deque
from typing import Optional
from fastapi import APIRouter, Depends
from app.schemas import ExpressionOut
from app.dependencies import get_history

router = APIRouter(prefix="/history", tags=["history"])

@router.get("", response_model=list[ExpressionOut])
def get_history_logs(
    limit: Optional[int] = None,
    history: deque = Depends(get_history)
):
    logs = list(history)
    if limit is not None and limit > 0:
        return logs[:limit]
    return logs

@router.delete("")
def clear_history_logs(history: deque = Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}