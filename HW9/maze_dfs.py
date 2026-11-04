from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

@dataclass(frozen=True)
class Point:
    row: int
    col: int

class MazeSolverDFS:
    """
    Object-Oriented Depth-First Search Maze Solver.
    Features visual ASCII rendering of dead ends, visited nodes, and final path.
    """
    WALL = 1
    PATH = 0

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.visited: Set[Point] = set()
        self.dead_ends: Set[Point] = set()

    def solve(self, start: Point, goal: Point) -> Optional[List[Point]]:
        path: List[Point] = []
        if self._dfs(start, goal, path):
            return path
        return None

    def _dfs(self, current: Point, goal: Point, path: List[Point]) -> bool:
        if not self._is_valid(current):
            return False

        self.visited.add(current)
        path.append(current)

        if current == goal:
            return True

        # 4-directional search order: Right, Down, Left, Up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nxt = Point(current.row + dr, current.col + dc)
            if nxt not in self.visited:
                if self._dfs(nxt, goal, path):
                    return True

        # Backtracking phase
        self.dead_ends.add(path.pop())
        return False

    def _is_valid(self, p: Point) -> bool:
        return (0 <= p.row < self.rows and 
                0 <= p.col < self.cols and 
                self.grid[p.row][p.col] != self.WALL)

    def render_visual(self, path: List[Point]) -> str:
        path_set = set(path)
        canvas = []
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                p = Point(r, c)
                if self.grid[r][c] == self.WALL:
                    row_str.append("██")
                elif p == path[0]:
                    row_str.append(" S")
                elif p == path[-1]:
                    row_str.append(" G")
                elif p in path_set:
                    row_str.append("••")
                elif p in self.dead_ends:
                    row_str.append(" xx")
                else:
                    row_str.append("  ")
            canvas.append("".join(row_str))
        return "\n".join(canvas)

if __name__ == "__main__":
    grid = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0]
    ]
    solver = MazeSolverDFS(grid)
    start, goal = Point(0, 0), Point(4, 5)
    result_path = solver.solve(start, goal)
    
    if result_path:
        print("Maze Solved via DFS Backtracking:")
        print(solver.render_visual(result_path))