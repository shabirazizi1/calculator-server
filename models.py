import re
from pydantic import BaseModel

class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        # Normalize display symbols to standard Python math operators
        normalized = self.expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        
        # Expand percentage arithmetic: e.g. "100 - 13.5%" -> "100 - (100 * 13.5 / 100)"
        expanded = re.sub(
            r'(\d+(?:\.\d+)?)\s*([\+\-])\s*(\d+(?:\.\d+)?)\s*%',
            r'\1 \2 (\1 * \3 / 100)',
            normalized
        )
        
        # Expand standalone percentages: e.g. "50%" -> "(50/100)"
        return re.sub(r'(\d+(?:\.\d+)?)\s*%', r'(\1/100)', expanded)

class CalculatorLog(BaseModel):
    timestamp: str
    expr: str
    result: float | int | str