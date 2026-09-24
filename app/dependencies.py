import re
from collections import deque
from fastapi import HTTPException, status
from app.schemas import ExpressionIn

# In-memory history state shared across requests
HISTORY_MAX = 50
history_db: deque = deque(maxlen=HISTORY_MAX)

def get_history() -> deque:
    """Dependency that injects the in-memory history storage."""
    return history_db

def expand_percent(payload: ExpressionIn) -> str:
    """Dependency that extracts and expands percentage operations in the expression."""
    try:
        raw_expr = payload.expr
        # Normalize display math operators
        normalized = raw_expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        
        # Expand relative percentage expressions: "100 - 6%" -> "100 - (100 * 6 / 100)"
        expanded = re.sub(
            r'(\d+(?:\.\d+)?)\s*([\+\-])\s*(\d+(?:\.\d+)?)\s*%',
            r'\1 \2 (\1 * \3 / 100)',
            normalized
        )
        
        # Expand standalone percentages: "50%" -> "(50/100)"
        return re.sub(r'(\d+(?:\.\d+)?)\s*%', r'(\1/100)', expanded)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to expand expression: {str(e)}"
        )