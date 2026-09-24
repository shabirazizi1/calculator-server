from datetime import datetime, timezone
from collections import deque
from fastapi import APIRouter, Depends
from app.schemas import ExpressionIn, ExpressionOut
from app.dependencies import expand_percent, get_history

router = APIRouter(tags=["calculator"])

@router.post("/calculate")
def calculate(
    payload: ExpressionIn,
    expanded_expr: str = Depends(expand_percent),
    history: deque = Depends(get_history)
):
    try:
        # Safely evaluate mathematical expression
        result = eval(expanded_expr, {"__builtins__": None}, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
    except Exception as e:
        return {"ok": False, "expr": payload.expr, "result": 0, "error": str(e)}

    # Build response object using inherited schema
    now_utc = datetime.now(timezone.utc).isoformat()
    log_entry = ExpressionOut(
        timestamp=now_utc,
        expr=payload.expr,
        result=result
    )
    history.appendleft(log_entry.model_dump())

    return {"ok": True, "expr": payload.expr, "result": result, "error": ""}