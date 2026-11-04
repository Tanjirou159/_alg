import time
from typing import List

class BitwiseNQueensDFS:
    """
    High-Performance Bitwise Backtracking DFS for N-Queens.
    Uses bitwise operators to compute column and diagonal conflicts in O(1) time.
    """
    def __init__(self, n: int = 8):
        self.n = n
        self.limit = (1 << n) - 1
        self.solutions: List[List[int]] = []

    def solve() -> List[List[int]]:
        self.solutions = []
        self._backtrack(0, 0, 0, 0, [])
        return self.solutions

    def _backtrack(self, row: int, cols: int, diag1: int, diag2: int, current_cols: List[int]):
        if cols == self.limit:
            self.solutions.append(list(current_cols))
            return

        # Bitmask representing available valid columns for the current row
        valid_positions = self.limit & ~(cols | diag1 | diag2)

        while valid_positions:
            # Isolate the lowest set bit
            bit = valid_positions & -valid_positions
            valid_positions -= bit

            col_index = bit.bit_length() - 1
            
            # Recurse with updated column and diagonal bitmasks
            self._backtrack(
                row + 1,
                cols | bit,
                (diag1 | bit) << 1,
                (diag2 | bit) >> 1,
                current_cols + [col_index]
            )

    def print_board(self, solution: List[int]):
        for col in solution:
            row = ["."] * self.n
            row[col] = "Q"
            print(" ".join(row))
        print()

if __name__ == "__main__":
    n = 8
    solver = BitwiseNQueensDFS(n)
    t0 = time.perf_counter()
    solutions = solver.solve()
    t1 = time.perf_counter()

    print(f"Found {len(solutions)} solutions for {n}-Queens in {(t1 - t0)*1000:.3f} ms.\n")
    print("Sample Solution Board:")
    solver.print_board(solutions[0])