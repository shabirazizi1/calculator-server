from collections import deque
from datetime import datetime, timezone
from fastapi import FastAPI
from asteval import Interpreter
from models import Expression, CalculatorLog

app = FastAPI()
aeval = Interpreter()
history = deque(maxlen=100)

@app.post("/calculate")
def calculate(payload: Expression):
    try:
        code = payload.expand_percent()
        result = aeval(code)
        
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": payload.expr, "result": "", "error": msg}
        
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        history.appendleft({"timestamp": timestamp, "expr": payload.expr, "result": result})
        
        return {"ok": True, "expr": payload.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": payload.expr, "error": str(e)}

@app.get("/history", response_model=list[CalculatorLog])
def get_history(limit: int = 10):
    return list(history)[:limit]

@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "cleared": True}