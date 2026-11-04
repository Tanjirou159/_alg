```python
# Test maze_dfs.py
from dataclasses import dataclass
from typing import List, Tuple, Optional, Set

@dataclass(frozen=True)
class Point:
    row: int
    col: int

class MazeSolverDFS:
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

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nxt = Point(current.row + dr, current.col + dc)
            if nxt not in self.visited:
                if self._dfs(nxt, goal, path):
                    return True

        self.dead_ends.add(path.pop())
        return False

    def _is_valid(self, p: Point) -> bool:
        return (0 <= p.row < self.rows and 
                0 <= p.col < self.cols and 
                self.grid[p.row][p.col] != self.WALL)

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
print("Maze DFS result:", result_path)


```

```text
Maze DFS result: [Point(row=0, col=0), Point(row=1, col=0), Point(row=2, col=0), Point(row=2, col=1), Point(row=2, col=2), Point(row=3, col=2), Point(row=3, col=3), Point(row=3, col=4), Point(row=4, col=4), Point(row=4, col=5)]


```

```python
# Test nqueens_bitwise.py
class BitwiseNQueensDFS:
    def __init__(self, n: int = 8):
        self.n = n
        self.limit = (1 << n) - 1
        self.solutions = []

    def solve(): # NOTICE THIS!
        pass


```

# Graph Search Algorithms & IC Circuit Routing Engine

A comprehensive suite of graph search algorithms, combinatorial solvers, and Electronic Design Automation (EDA) circuit routing algorithms implemented in Python.

---

## Table of Contents

1. [Project Structure](https://www.google.com/search?q=%23project-structure)
2. [Algorithms Overview](https://www.google.com/search?q=%23algorithms-overview)
* [1. Rat in a Maze (DFS with Backtracking)](https://www.google.com/search?q=%231-rat-in-a-maze-dfs-with-backtracking)
* [2. Wolf, Goat, and Cabbage River Crossing (BFS)](https://www.google.com/search?q=%232-wolf-goat-and-cabbage-river-crossing-bfs)
* [3. 8-Queens Problem (Bitwise DFS)](https://www.google.com/search?q=%233-8-queens-problem-bitwise-dfs)
* [4. NPC Pathfinding to Player (8-Directional A* Search)](https://www.google.com/search?q=%234-npc-pathfinding-to-player-8-directional-a-search)
* [5. IC Design Circuit Routing (EDA Routers)](https://www.google.com/search?q=%235-ic-design-circuit-routing-eda-routers)


3. [EDA Routing Methods Comparison](https://www.google.com/search?q=%23eda-routing-methods-comparison)
4. [Theoretical Complexity Analysis](https://www.google.com/search?q=%23theoretical-complexity-analysis)
5. [Installation & Execution Guide](https://www.google.com/search?q=%23installation--execution-guide)

---

## Project Structure

```text
search_engine_suite/
├── algorithms/
│   ├── maze_dfs.py          # Object-oriented DFS maze solver with backtracking & ASCII visualization
│   ├── river_bfs.py         # Bitmask-encoded BFS river crossing solver with state rendering
│   ├── nqueens_bitwise.py   # High-performance bitwise DFS solver for N-Queens
│   ├── npc_astar_8dir.py    # 8-directional A* search with terrain cost matrices
│   └── ic_routing_eda.py    # EDA circuit routing algorithms (Lee, A*, Hadlock, Line Search)
└── README.md                # Project documentation and theoretical analysis

```

---

## Algorithms Overview

### 1. Rat in a Maze (DFS with Backtracking)

* **Script**: `algorithms/maze_dfs.py`
* **Algorithm**: Depth-First Search (DFS) with explicit backtracking.
* **Problem Description**: Given an $M \times N$ grid with open cells (`0`) and impassable walls (`1`), find a contiguous path from start position $S = (0, 0)$ to exit $T = (M-1, N-1)$.
* **Search Mechanism**:
* Traverses nodes using standard direction vectors: $\text{Right } (0, 1)$, $\text{Down } (1, 0)$, $\text{Left } (0, -1)$, and $\text{Up } (-1, 0)$.
* Tracks visited nodes in a set to prevent infinite loops.
* When encountering a boundary condition, obstacle, or previously visited node, the search backtracks by popping the current node off the trajectory stack and exploring alternate candidate edges.



```text
Visual ASCII Rendering Example:
S  ██                  
•• ██    ██ ██         
••••••    ██           
██ ██••••••    ██      
      ██•• G           
(Legend: S = Start, G = Goal, •• = Path, ██ = Wall)

```

---

### 2. Wolf, Goat, and Cabbage River Crossing (BFS)

* **Script**: `algorithms/river_bfs.py`
* **Algorithm**: Bitmask-encoded Breadth-First Search (BFS).
* **Problem Description**: A farmer must transfer a wolf, a goat, and a cabbage from the left bank of a river to the right bank using a boat that holds the farmer and at most one item.
* Conflict rules: The wolf and goat cannot be left unattended; the goat and cabbage cannot be left unattended.


* **State Representation & Bitmask Logic**:
* State is encoded as a 4-bit unsigned integer $b_3 b_2 b_1 b_0$:

$$\text{State} = (F \cdot 2^3) + (W \cdot 2^2) + (G \cdot 2^1) + (C \cdot 2^0)$$



where $0$ represents the Left Bank and $1$ represents the Right Bank.
* Safety condition evaluation via bitwise operations:

$$\text{Safe}(s) = \neg \Big(\big((W == G) \land (F \neq W)\big) \lor \big((G == C) \land (F \neq G)\big)\Big)$$




* **Optimality**: BFS guarantees finding the minimum-step sequence to reach the goal state `0b1111` (7 transitions).

```text
State Transition Output:
Step 0: [F W G C] ~~~~~ RIVER ~~~~~ [       ]
Step 1: [  W   C] ~~~~~ RIVER ~~~~~ [F   G  ]
Step 2: [F W   C] ~~~~~ RIVER ~~~~~ [    G  ]
Step 3: [      C] ~~~~~ RIVER ~~~~~ [F W G  ]
Step 4: [F     G] ~~~~~ RIVER ~~~~~ [  W   C]
Step 5: [      G] ~~~~~ RIVER ~~~~~ [F W   C]
Step 6: [F     G] ~~~~~ RIVER ~~~~~ [  W   C]
Step 7: [       ] ~~~~~ RIVER ~~~~~ [F W G C]

```

---

### 3. 8-Queens Problem (Bitwise DFS)

* **Script**: `algorithms/nqueens_bitwise.py`
* **Algorithm**: Bitwise Depth-First Search with Backtracking.
* **Problem Description**: Place 8 non-attacking queens on an $8 \times 8$ chessboard such that no two queens occupy the same row, column, or diagonal.
* **Bitwise Conflict Acceleration**:
* Rather than checking candidate positions with nested loops, three integer bitmasks track board threats:
1. `cols`: Occupied column bitmask.
2. `diag1`: Left-diagonal threat bitmask (shifted left `<< 1` at each depth step).
3. `diag2`: Right-diagonal threat bitmask (shifted right `>> 1` at each depth step).


* Available valid columns for a row are calculated in $O(1)$ time:

$$\text{Available} = \text{Limit} \land \neg (\text{cols} \lor \text{diag1} \lor \text{diag2})$$


* The lowest set bit is isolated instantly via two's complement: $\text{bit} = \text{Available} \land (-\text{Available})$.



```text
Sample 8-Queens Board Solution:
Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .

```

---

### 4. NPC Pathfinding to Player (8-Directional A* Search)

* **Script**: `algorithms/npc_astar_8dir.py`
* **Algorithm**: Informed $A^*$ Search with Variable Terrain Costs and 8-Way Diagonal Traversal.
* **Problem Description**: A game NPC must navigate non-uniform terrain (flat ground, mud, obstacles) to catch a moving player along an optimal cost path.
* **Evaluation Function**:

$$f(n) = g(n) + h(n)$$


* $g(n)$: Accumulated exact path cost from start to node $n$, taking into account cardinal movement step cost ($1.0$), diagonal step cost ($\approx 1.414$), and cell terrain weight multipliers.
* $h(n)$: **Octile Distance Heuristic** (admissible and consistent for 8-directional grids):

$$h(n) = D_1 \cdot (\Delta x + \Delta y) + (D_2 - 2D_1) \cdot \min(\Delta x, \Delta y)$$



where $D_1 = 1.0$, $D_2 = \sqrt{2} \approx 1.414$, $\Delta x = \vert{}x_n - x_{\text{goal}}\vert{}$, and $\Delta y = \vert{}y_n - y_{\text{goal}}\vert{}$.



---

### 5. IC Design Circuit Routing (EDA Routers)

* **Script**: `algorithms/ic_routing_eda.py`
* **Context**: Electronic Design Automation (EDA) physical design routing connects terminal pins on a microchip layout layer while navigating around macro blockages, power rails, and existing net wires.

```text
EDA Routing Architecture & Flow:

      [Source Pin S] -----------------------------------> [Target Pin T]
            |                                                   |
            +--> 1. Lee's Router (BFS Wavefront Expansion) ------> Minimal Wire Length
            |
            +--> 2. A* Router (Guided Wavefront Search) --------> Faster Convergence
            |
            +--> 3. Hadlock's Router (Detour Number Optimization) -> Low Cell Expansion
            |
            +--> 4. Line Search Router (Escape Ray Projection) --> Gridless / Fast

```

---

## EDA Routing Methods Comparison

| Routing Algorithm | Search Strategy | Wire Length Optimality | Search Space / Memory | Best Suited EDA Phase |
| --- | --- | --- | --- | --- |
| **Lee's Wavefront Router** | Breadth-First Search (BFS) | **Guaranteed Optimal** | $O(M \times N)$ High | Critical nets requiring exact shortest wire length. |
| **$A^*$ Grid Router** | Best-First Search with Manhattan $h(n)$ | **Guaranteed Optimal** | Reduced search space | Point-to-point standard cell routing in detailed routing. |
| **Hadlock's Detour Router** | Min-Detour Number Priority Queue | **Guaranteed Optimal** | $O(M \times N)$ Worst case | Global/Detailed grid routing with few local blockages. |
| **Mikami-Tabuchi Line Search** | Escape Ray Projection & Intersection | Near-Optimal / Heuristic | $O(L)$ Very Low | Early-stage interactive routing & unconstrained channel routing. |

### Detailed Algorithm Descriptions

1. **Lee's Wavefront Algorithm**
* **Expansion Phase**: Expands distance labels ($1, 2, 3, \dots$) outward in concentric rings from source terminal $S$ until target terminal $T$ is reached.
* **Backtracking Phase**: Traces back from $T$ to $S$ along cells with strictly decreasing values ($d, d-1, d-2, \dots$).
* *Trade-off*: Expands every reachable node in all directions; memory consuming for large IC dies.


2. **$A^*$ Grid Router**
* Incorporates Manhattan distance heuristic $h(n) = \vert{}x_n - x_T\vert{} + \vert{}y_n - y_T\vert{}$ into the wavefront expansion.
* Directs search focus toward the destination pin $T$, pruning up to 80% of unnecessary node expansions compared to Lee's algorithm.


3. **Hadlock's Detour Algorithm**
* Redefines path cost using the **Detour Index** $d(n)$:
* Moving closer to target $T \Rightarrow \text{Detour } +0$
* Moving away from target $T \Rightarrow \text{Detour } +1$


* Processes grid cells in order of increasing detour count $d(n)$. When no obstacles block the straight path, Hadlock's algorithm reaches the target without exploring sideways nodes.


4. **Mikami-Tabuchi Line Search Router**
* Instead of filling a 2D matrix grid, projects horizontal and vertical line segments (escape lines) from source $S$ and target $T$ until they hit obstacles.
* Generates secondary perpendicular escape lines from points on the primary lines until line segments from $S$ and $T$ intersect.
* Reconstructs the net path by linking the intersecting line segments.



---

## Theoretical Complexity Analysis

| Problem Domain | Primary Algorithm | Time Complexity | Space Complexity |
| --- | --- | --- | --- |
| **Rat in a Maze** | DFS with Backtracking | $O(V + E) \approx O(M \times N)$ | $O(M \times N)$ recursion stack |
| **River Crossing** | Bitmask BFS | $O(2^B)$ where $B = 4$ bits | $O(2^B)$ state queue |
| **8-Queens Problem** | Bitwise DFS | $O(N!)$ worst case | $O(N)$ recursion depth |
| **NPC Pathfinding** | 8-Directional $A^*$ | $O(E \log V)$ worst case | $O(V)$ open/closed sets |
| **IC Grid Routing** | Lee's Router | $O(M \times N)$ | $O(M \times N)$ distance grid |
| **IC Grid Routing** | Hadlock's Router | $O(M \times N)$ worst case | $O(M \times N)$ detour map |
| **IC Line Routing** | Mikami-Tabuchi | $O(L^2)$ where $L$ = escape lines | $O(L)$ line list |

---

## Installation & Execution Guide

### Prerequisites

* Python 3.8 or higher installed.

### Running the Modules

Execute any individual algorithm module directly:

```bash
# 1. Run Maze DFS Solver
python algorithms/maze_dfs.py

# 2. Run River Crossing BFS Solver
python algorithms/river_bfs.py

# 3. Run Bitwise N-Queens DFS Solver
python algorithms/nqueens_bitwise.py

# 4. Run 8-Directional NPC A* Pathfinding
python algorithms/npc_astar_8dir.py

# 5. Run EDA Circuit Routers Benchmark
python algorithms/ic_routing_eda.py

```