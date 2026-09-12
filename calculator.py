# calculator.py
import re

_percent_pair = re.compile(r"""
    (?P<a>\d+(?:\.\d+)?)
    \s*(?P<op>[+\-*/])\s*
    (?P<b>\d+(?:\.\d+)?)%
""", re.VERBOSE)

# NEW: Regex to match standalone percentages (e.g., "100%")
_standalone_percent = re.compile(r"(\d+(?:\.\d+)?)%")

def expand_percent(expr: str) -> str:
    """Handle A op B% and standalone N% patterns."""
    s = expr
    while True:
        # Replace A op B%
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b = m.group("a", "op", "b")
        if op in "+-":
            repl = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            repl = f"{a} * ({b}/100)"
        else:
            repl = f"{a} / ({b}/100)"
        s = s[:m.start()] + repl + s[m.end():]
    
    # NEW: Handle standalone percentages left in the string
    s = _standalone_percent.sub(r"(\1/100)", s)
        
    return s
