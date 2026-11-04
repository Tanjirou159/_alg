from collections import deque
from typing import List, Tuple, Dict

class BitmaskRiverBFS:
    """
    Bitmask-Encoded BFS River Crossing Solver.
    Uses binary state vectors: (Farmer, Wolf, Goat, Cabbage) where 0=Left, 1=Right.
    """
    FARMER  = 1 << 3  # 0b1000
    WOLF    = 1 << 2  # 0b0100
    GOAT    = 1 << 1  # 0b0010
    CABBAGE = 1 << 0  # 0b0001

    START_STATE = 0b0000
    GOAL_STATE  = 0b1111

    @classmethod
    def is_safe(cls, state: int) -> bool:
        farmer_side = bool(state & cls.FARMER)
        wolf_side = bool(state & cls.WOLF)
        goat_side = bool(state & cls.GOAT)
        cabbage_side = bool(state & cls.CABBAGE)

        # Wolf eats Goat if Farmer is on other side
        if wolf_side == goat_side and farmer_side != wolf_side:
            return False
        # Goat eats Cabbage if Farmer is on other side
        if goat_side == cabbage_side and farmer_side != goat_side:
            return False
        return True

    @classmethod
    def solve(cls) -> List[int]:
        queue = deque([(cls.START_STATE, [cls.START_STATE])])
        visited = {cls.START_STATE}

        items = [cls.WOLF, cls.GOAT, cls.CABBAGE]

        while queue:
            curr, path = queue.popleft()
            if curr == cls.GOAL_STATE:
                return path

            farmer_present = bool(curr & cls.FARMER)
            next_candidates = []

            # Option A: Farmer moves alone
            next_candidates.append(curr ^ cls.FARMER)

            # Option B: Farmer carries one item located on the same bank
            for item in items:
                item_present = bool(curr & item)
                if farmer_present == item_present:
                    next_candidates.append(curr ^ cls.FARMER ^ item)

            for nxt in next_candidates:
                if cls.is_safe(nxt) and nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))

        return []

    @classmethod
    def render_ascii_transition(cls, state: int) -> str:
        left, right = [], []
        names = [("F", cls.FARMER), ("W", cls.WOLF), ("G", cls.GOAT), ("C", cls.CABBAGE)]
        for symbol, mask in names:
            if state & mask:
                right.append(symbol)
            else:
                left.append(symbol)
        
        left_str = f"[{' '.join(left):<7}]"
        right_str = f"[{' '.join(right):<7}]"
        return f"{left_str} ~~~~~ RIVER ~~~~~ {right_str}"

if __name__ == "__main__":
    solution = BitmaskRiverBFS.solve()
    print(f"Optimal BFS Path ({len(solution) - 1} steps):\n")
    for step, st in enumerate(solution):
        print(f"Step {step}: {BitmaskRiverBFS.render_ascii_transition(st)}")