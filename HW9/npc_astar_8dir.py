import heapq
import math
from typing import List, Tuple, Dict, Optional

class AStarNPC8Way:
    """
    8-Directional A* Pathfinding for Dynamic Game Terrain.
    Supports diagonal movements with Euclidean heuristic and variable cost terrains.
    """
    # Movement vectors and costs: Cardinal = 1.0, Diagonal = sqrt(2) ≈ 1.414
    DIRECTIONS = [
        (0, 1, 1.0), (1, 0, 1.0), (0, -1, 1.0), (-1, 0, 1.0),
        (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)
    ]

    def __init__(self, terrain_grid: List[List[float]]):
        self.grid = terrain_grid
        self.rows = len(terrain_grid)
        self.cols = len(terrain_grid[0])

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        # Octile Distance for 8-directional grids
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return (dx + dy) + (1.414 - 2) * min(dx, dy)

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[Tuple[List[Tuple[int, int]], float]]:
        open_set = []
        heapq.heappush(open_set, (self._heuristic(start, goal), 0.0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}

        while open_set:
            f, current_g, current = heapq.heappop(open_set)

            if current == goal:
                # Path Reconstruction
                path = []
                curr = goal
                while curr in came_from:
                    path.append(curr)
                    curr = came_from[curr]
                path.append(start)
                path.reverse()
                return path, g_score[goal]

            if current_g > g_score.get(current, float('inf')):
                continue

            r, c = current
            for dr, dc, base_cost in self.DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    terrain_multiplier = self.grid[nr][nc]
                    if terrain_multiplier < 0:  # Negative value represents impassable obstacle
                        continue

                    step_cost = base_cost * terrain_multiplier
                    tentative_g = current_g + step_cost
                    neighbor = (nr, nc)

                    if tentative_g < g_score.get(neighbor, float('inf')):
                        g_score[neighbor] = tentative_g
                        came_from[neighbor] = current
                        f_score = tentative_g + self._heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, tentative_g, neighbor))

        return None

if __name__ == "__main__":
    # 1.0 = Flat ground, 3.0 = Rough terrain, -1.0 = Wall
    map_matrix = [
        [1.0, 1.0, 1.0, 1.0, 1.0],
        [-1.0, -1.0, 3.0, -1.0, 1.0],
        [1.0, 3.0, 3.0, 1.0, 1.0],
        [1.0, -1.0, -1.0, -1.0, 1.0],
        [1.0, 1.0, 1.0, 1.0, 1.0]
    ]

    npc_pathfinder = AStarNPC8Way(map_matrix)
    path, total_cost = npc_pathfinder.find_path((0, 0), (4, 4))
    print(f"8-Directional Path: {path}")
    print(f"Total Movement Cost: {total_cost:.3f}")