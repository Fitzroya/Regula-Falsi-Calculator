def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Regula Falsi (False Position) Method with Relative Error
    
    Parameters:
    f: function
    a, b: interval [a, b] with f(a)*f(b) < 0
    tol: tolerance for approximate percent relative error (as decimal, e.g., 0.05 = 5%)
    max_iter: maximum number of iterations
    
    Returns:
    (root, iterations_table, message)
    """
    
    iterations = []
    fa = f(a)
    fb = f(b)
    c_old = a
    error = None
    
    if fa * fb >= 0:
        return None, [], "No sign change in interval"
    
    for i in range(max_iter):
        # Calculate false position
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        
        # Calculate approximate percent relative error
        if i > 0:
            error = abs((c - c_old) / c) * 100
        else:
            error = None
        
        # Store iteration data (using xr and fxr keys)
        iterations.append({
            'iteration': i + 1,
            'a': a,
            'b': b,
            'xr': c,           # <-- KEY: xr (not c)
            'fa': fa,
            'fb': fb,
            'fxr': fc,         # <-- KEY: fxr (not fc)
            'error': error
        })
        
        # Check stopping criteria
        if fc == 0:
            return c, iterations, f"Exact root found after {i+1} iterations"
        
        if error is not None and error < tol:
            return c, iterations, f"Converged! Final relative error = {error:.4f}% < {tol*100}%"
        
        # Update interval
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        c_old = c
    
    # If max iterations reached
    final_error = iterations[-1]['error'] if iterations[-1]['error'] is not None else float('inf')
    return c, iterations, f"Max iterations ({max_iter}) reached. Final error = {final_error:.4f}%"