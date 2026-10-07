def sym_diff(expr, var='x'):
    """Recursively computes symbolic derivative d(expr)/d(var)."""
    # Constant Rule: d/dx(c) = 0
    if isinstance(expr, (int, float)):
        return 0
    
    # Variable Rule: d/dx(x) = 1, d/dx(y) = 0
    if isinstance(expr, str):
        return 1 if expr == var else 0
    
    # Compound Expression Operations
    if isinstance(expr, tuple):
        op = expr[0]
        
        if op == '+':
            # Sum Rule: (u + v)' = u' + v'
            return ('+', sym_diff(expr[1], var), sym_diff(expr[2], var))
            
        elif op == '-':
            # Difference Rule: (u - v)' = u' - v'
            return ('-', sym_diff(expr[1], var), sym_diff(expr[2], var))
            
        elif op == '*':
            # Product Rule: (u * v)' = u' * v + u * v'
            u, v = expr[1], expr[2]
            return ('+', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var)))
            
        elif op == '/':
            # Quotient Rule: (u / v)' = (u' * v - u * v') / (v ** 2)
            u, v = expr[1], expr[2]
            du, dv = sym_diff(u, var), sym_diff(v, var)
            num = ('-', ('*', du, v), ('*', u, dv))
            den = ('**', v, 2)
            return ('/', num, den)
            
        elif op == '**':
            # Power Rule: (u ** n)' = n * (u ** (n - 1)) * u'
            u, n = expr[1], expr[2]
            if isinstance(n, (int, float)):
                return ('*', ('*', n, ('**', u, n - 1)), sym_diff(u, var))

    raise ValueError(f"Unsupported expression: {expr}")


def simplify(expr):
    """Optional basic expression tree simplifier."""
    if not isinstance(expr, tuple):
        return expr
    
    op, u, v = expr[0], simplify(expr[1]), simplify(expr[2])
    
    if op == '+':
        if u == 0: return v
        if v == 0: return u
    elif op == '*':
        if u == 0 or v == 0: return 0
        if u == 1: return v
        if v == 1: return u
    elif op == '**':
        if v == 1: return u
        if v == 0: return 1
        
    return (op, u, v)

# Example: d/dx (x^3 + 2x)
# Representation: ('+', ('**', 'x', 3), ('*', 2, 'x'))
expr = ('+', ('**', 'x', 3), ('*', 2, 'x'))
derivative = sym_diff(expr, 'x')

print("Raw Derivative:       ", derivative)
print("Simplified Derivative:", simplify(derivative))