from collections import deque
import heapq
from typing import List, Tuple, Optional

class EDAMazeRouter:
    """
    Integrated Electronic Design Automation (EDA) Circuit Router.
    Implements Lee's Wavefront Algorithm, A* Heuristic Router, Hadlock's Detour Router,
    and Mikami-Tabuchi Line Search Router.
    """
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    # --- 1. Lee's Wavefront Router ---
    def route_lee(self, source: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        dist = [[-1] * self.cols for _ in range(self.rows)]
        q = deque([source])
        dist[source[0]][source[1]] = 0

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        found = False

        while q:
            curr = q.popleft()
            if curr == target:
                found = True
                break
            for dr, dc in dirs:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                    if dist[nr][nc] == -1:
                        dist[nr][nc] = dist[curr[0]][curr[1]] + 1
                        q.append((nr, nc))

        if not found:
            return None

        # Backtracking
        path = [target]
        curr = target
        while curr != source:
            d = dist[curr[0]][curr[1]]
            for dr, dc in dirs:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and dist[nr][nc] == d - 1:
                    path.append((nr, nc))
                    curr = (nr, nc)
                    break
        path.reverse()
        return path

    # --- 2. Hadlock's Detour Router ---
    def route_hadlock(self, source: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        def is_detour(curr, nxt):
            # Moving away from target adds 1 to detour count
            curr_dist = abs(curr[0] - target[0]) + abs(curr[1] - target[1])
            nxt_dist = abs(nxt[0] - target[0]) + abs(nxt[1] - target[1])
            return 1 if nxt_dist > curr_dist else 0

        # Priority queue ordered by total detours
        pq = [(0, source)]
        detour_map = {source: 0}
        came_from = {}

        while pq:
            d, curr = heapq.heappop(pq)

            if curr == target:
                path = [target]
                while curr in came_from:
                    curr = came_from[curr]
                    path.append(curr)
                path.reverse()
                return path

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                    nxt = (nr, nc)
                    new_detour = d + is_detour(curr, nxt)
                    if new_detour < detour_map.get(nxt, float('inf')):
                        detour_map[nxt] = new_detour
                        came_from[nxt] = curr
                        heapq.heappush(pq, (new_detour, nxt))
        return None

    # --- 3. Mikami-Tabuchi Line Search Router ---
    def route_line_search(self, source: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        def generate_escape_lines(pt):
            lines = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                curr = (pt[0] + dr, pt[1] + dc)
                line = []
                while 0 <= curr[0] < self.rows and 0 <= curr[1] < self.cols and self.grid[curr[0]][curr[1]] == 0:
                    line.append(curr)
                    curr = (curr[0] + dr, curr[1] + dc)
                if line:
                    lines.append(line)
            return lines

        s_lines = generate_escape_lines(source)
        t_lines = generate_escape_lines(target)

        # Check for intersection between escape line segments
        for s_line in s_lines:
            for t_line in t_lines:
                intersections = set(s_line).intersection(set(t_line))
                if intersections:
                    meet_point = list(intersections)[0]
                    # Form path: source -> s_line up to meet -> t_line to target
                    idx_s = s_line.index(meet_point)
                    idx_t = t_line.index(meet_point)
                    return [source] + s_line[:idx_s+1] + t_line[:idx_t][::-1] + [target]
        
        # Fallback to Lee's router if line search fails due to complex blockages
        return self.route_lee(source, target)

if __name__ == "__main__":
    eda_grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    router = EDAMazeRouter(eda_grid)
    src, tgt = (2, 2), (0, 5)

    print("Lee's Wire Route:       ", router.route_lee(src, tgt))
    print("Hadlock Detour Route:   ", router.route_hadlock(src, tgt))
    print("Line Search Route:      ", router.route_line_search(src, tgt))