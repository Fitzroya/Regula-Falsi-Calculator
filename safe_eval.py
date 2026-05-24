import math

ALLOWED_FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'exp': math.exp,
    'log': math.log,
    'log10': math.log10,
    'sqrt': math.sqrt,
    'abs': abs,
    'pi': math.pi,
    'e': math.e
}

def safe_eval_function(func_str, x):
    """Safely evaluate a mathematical function using Python syntax"""
    try:
        safe_dict = {
            'x': x,
            '__builtins__': {},
            **ALLOWED_FUNCTIONS
        }
        result = eval(func_str, safe_dict, {})
        return float(result)
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax. Use Python math: x**2, exp(x), sin(x)")
    except NameError as e:
        raise ValueError(f"Unknown function. Use: sin, cos, exp, log, sqrt")
    except Exception as e:
        raise ValueError(f"Error: {e}")