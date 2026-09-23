import contextlib
import io
import itertools

from sat import solve_sat_truth_table


def evaluate(formula_str, env):
    return bool(eval(formula_str, {"__builtins__": None}, env))


def run_solver(variables, formula_str):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = solve_sat_truth_table(variables, formula_str)
    return result, buf.getvalue()


def check_solver(variables, formula_str, expected_count):
    result, output = run_solver(variables, formula_str)

    assert len(result) == expected_count, (
        f"{formula_str}: expected {expected_count} satisfying assignment(s), "
        f"got {len(result)}: {result}"
    )

    assert "SATISFIABLE" in output or "UNSATISFIABLE" in output

    all_assignments = [
        dict(zip(variables, combo))
        for combo in itertools.product([True, False], repeat=len(variables))
    ]
    returned = {tuple(sorted(a.items())) for a in result}

    for env in all_assignments:
        expected = evaluate(formula_str, env)
        is_returned = tuple(sorted(env.items())) in returned
        assert expected == is_returned, (
            f"{formula_str}: assignment {env} "
            f"(evaluates to {expected}) incorrectly "
            f"{'missing from' if expected else 'included in'} result"
        )

    return result, output


def test_example_formula():
    result, output = check_solver(
        ["A", "B", "C"],
        "(A or B) and (not A or C) and (not B or not C)",
        2,
    )
    print(f"example: {len(result)} satisfying, SATISFIABLE printed: "
          f"{'SATISFIABLE' in output}")


def test_unsat():
    result, output = check_solver(["A"], "A and not A", 0)
    assert "UNSATISFIABLE" in output


def test_tautology():
    check_solver(["A"], "A or not A", 2)


def test_unit():
    check_solver(["A", "B"], "A and not B", 1)


def test_unused_variable():
    check_solver(["A", "B"], "A", 2)


def test_empty_variables():
    check_solver([], "True", 1)


def test_five_variables():
    check_solver(
        ["A", "B", "C", "D", "E"],
        "(A or B or C) and (not A or D) and (B or not D or E) and (not C or not E)",
        11,
    )


def main():
    tests = [
        test_example_formula,
        test_unsat,
        test_tautology,
        test_unit,
        test_unused_variable,
        test_empty_variables,
        test_five_variables,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\nAll {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
