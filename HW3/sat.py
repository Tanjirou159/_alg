import itertools

def solve_sat_truth_table(variables, formula_str):
    """
    Systematically enumerates all 2^N variable assignments to build a 
    truth table and determine satisfiability for a Boolean expression.
    
    :param variables: List of variable names (e.g., ['A', 'B', 'C'])
    :param formula_str: Boolean expression using Python operators ('and', 'or', 'not')
    :return: List of satisfying truth assignments (models)
    """
    n = len(variables)
    satisfying_assignments = []

    # Print truth table header
    header = " | ".join(f"{v:^5}" for v in variables) + " | " + f"{'Result':^7}"
    print(f"Formula: {formula_str}")
    print(header)
    print("-" * len(header))

    # Systematically iterate through all 2^N truth value combinations
    for values in itertools.product([True, False], repeat=n):
        # Bind variables to current truth assignment
        environment = dict(zip(variables, values))
        
        # Evaluate formula within restricted environment
        result = bool(eval(formula_str, {"__builtins__": {}}, environment))
        
        if result:
            satisfying_assignments.append(environment)

        # Print current truth table row
        row_str = " | ".join(f"{str(val):^5}" for val in values) + f" | {str(result):^7}"
        print(row_str)

    print("-" * len(header))
    
    # Verdict
    if satisfying_assignments:
        print(f"Status: SATISFIABLE ({len(satisfying_assignments)} satisfying model(s) found)")
        print("Models:")
        for model in satisfying_assignments:
            print(" ", model)
    else:
        print("Status: UNSATISFIABLE (No satisfying assignment exists)")

    return satisfying_assignments


# --- Demonstration ---
if __name__ == "__main__":
    # Example 1: Satisfiable formula (SAT)
    # Formula: (A or B) and (not A or C) and (not B or not C)
    print("=== Test Case 1 ===")
    vars_1 = ['A', 'B', 'C']
    expr_1 = "(A or B) and (not A or C) and (not B or not C)"
    solve_sat_truth_table(vars_1, expr_1)

    print("\n" + "=" * 40 + "\n")

    # Example 2: Unsatisfiable formula (UNSAT)
    # Formula: A and not A
    print("=== Test Case 2 ===")
    vars_2 = ['A']
    expr_2 = "A and not A"
    solve_sat_truth_table(vars_2, expr_2)