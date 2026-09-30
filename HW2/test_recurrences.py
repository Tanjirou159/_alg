import math

from recurrences import (
    RECURRENCES,
    closed_form,
    closed_form_divide,
    closed_form_decrease,
    iterative_simulate,
)


def test_decrease_factor_one():
    assert closed_form_decrease(1, 8, 1) == 1
    assert closed_form_decrease(1, 8, 2) == 9
    assert closed_form_decrease(1, 8, 10) == 73
    assert closed_form_decrease(1, 8, 100) == 793


def test_decrease_factor_two():
    assert closed_form_decrease(2, 9, 1) == 1
    assert closed_form_decrease(2, 9, 2) == 11
    assert closed_form_decrease(2, 9, 3) == 31
    assert closed_form_decrease(2, 9, 10) == 5111


def test_divide_factor_two():
    assert closed_form_divide(2, 1, 1) == 1
    assert closed_form_divide(2, 1, 2) == 3
    assert closed_form_divide(2, 1, 4) == 7
    assert closed_form_divide(2, 1, 1024) == 2047


def test_divide_factor_one():
    assert closed_form_divide(1, 1, 1) == 1
    assert closed_form_divide(1, 1, 2) == 2
    assert closed_form_divide(1, 1, 4) == 3
    assert closed_form_divide(1, 1, 1024) == 11


def test_expected_big_o():
    assert RECURRENCES["T(n) = T(n-1) + 8"]["big_o"] == "O(n)"
    assert RECURRENCES["T(n) = 2 T(n-1) + 9"]["big_o"] == "O(2^n)"
    assert RECURRENCES["T(n) = 2 T(n/2) + 1"]["big_o"] == "O(n)"
    assert RECURRENCES["T(n) = T(n/2) + 1"]["big_o"] == "O(log n)"


def test_hand_checked_values():
    assert closed_form("T(n) = T(n-1) + 8", 7) == 49
    assert closed_form("T(n) = 2 T(n-1) + 9", 7) == 631
    assert closed_form("T(n) = 2 T(n/2) + 1", 8) == 15
    assert closed_form("T(n) = T(n/2) + 1", 8) == 4


def test_closed_form_matches_simulation():
    for recurrence in RECURRENCES:
        spec = RECURRENCES[recurrence]
        if spec["kind"] == "decrease":
            ns = range(1, 41)
        else:
            ns = [2 ** k for k in range(0, 11)]
        for n in ns:
            exact = closed_form(recurrence, n)
            simulated = iterative_simulate(recurrence, n)
            assert exact == simulated, (
                f"{recurrence} at n={n}: closed form {exact} "
                f"!= simulated {simulated}"
            )


def test_growth_rate_ratios():
    assert closed_form("T(n) = T(n-1) + 8", 32) / closed_form("T(n) = T(n-1) + 8", 16) < 3
    assert closed_form("T(n) = 2 T(n-1) + 9", 32) / closed_form("T(n) = 2 T(n-1) + 9", 16) > 1000
    assert closed_form("T(n) = 2 T(n/2) + 1", 1024) / closed_form("T(n) = 2 T(n/2) + 1", 512) < 3
    assert closed_form("T(n) = T(n/2) + 1", 1024) - closed_form("T(n) = T(n/2) + 1", 512) == 1


def test_log_base_two_identity():
    for k in range(0, 11):
        n = 2 ** k
        assert closed_form("T(n) = T(n/2) + 1", n) == int(math.log2(n)) + 1


def main():
    tests = [
        test_decrease_factor_one,
        test_decrease_factor_two,
        test_divide_factor_two,
        test_divide_factor_one,
        test_expected_big_o,
        test_hand_checked_values,
        test_closed_form_matches_simulation,
        test_growth_rate_ratios,
        test_log_base_two_identity,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\nAll {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
