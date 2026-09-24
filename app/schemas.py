from pydantic import BaseModel

class BaseExpression(BaseModel):
    expr: str

class ExpressionIn(BaseExpression):
    """Request payload schema for /calculate."""
    pass

# Alias for backwards compatibility
Expression = ExpressionIn

class ExpressionOut(BaseExpression):
    """Response payload schema for /history logs."""
    timestamp: str
    result: float | int | str

# Alias for backwards compatibility
CalculatorLog = ExpressionOut