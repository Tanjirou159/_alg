import itertools

def solve_sat_truth_table(variables, formula_str):
    """
    Solves SAT for a given Boolean expression by systematically generating its truth table.
    
    :param variables: List of string variable names, e.g., ['A', 'B', 'C']
    :param formula_str: Python boolean expression string using standard operators 
                        ('and', 'or', 'not'), e.g., "(A or B) and (not A or C)"
    :return: List of dictionaries representing satisfying truth assignments
    """
    n = len(variables)
    header = " | ".join(f"{var:^5}" for var in variables) + " | Result"
    divider = "-" * len(header)
    
    print(header)
    print(divider)
    
    satisfying_assignments = []
    
    # 1. Systematically generate all 2^n truth value assignments
    for combination in itertools.product([True, False], repeat=n):
        # Map variables to their corresponding truth value in this row
        env = dict(zip(variables, combination))
        
        # 2. Evaluate the expression under the environment
        result = bool(eval(formula_str, {"__builtins__": None}, env))
        
        # 3. Print table row
        row_str = " | ".join(f"{str(val):^5}" for val in combination)
        print(f"{row_str} | {str(result):^6}")
        
        if result:
            satisfying_assignments.append(env)
            
    print(divider)
    
    # 4. Determine satisfiability
    if satisfying_assignments:
        print(f"SATISFIABLE: Found {len(satisfying_assignments)} satisfying assignment(s).")
    else:
        print("UNSATISFIABLE: No truth assignment satisfies the formula.")
        
    return satisfying_assignments


if __name__ == "__main__":
    # Example expression: (A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)
    vars_list = ['A', 'B', 'C']
    expr = "(A or B) and (not A or C) and (not B or not C)"
    
    print(f"Formula: {expr}\n")
    solve_sat_truth_table(vars_list, expr)