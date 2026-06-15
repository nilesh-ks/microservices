# Pattern 1 — DFS (Depth-First Search)

**One-liner:** Go DEEP first, mark visited, backtrack. Recursion (ya explicit `Deque` stack) se reachable nodes enumerate karo, components count karo, cycles detect karo, ya order banao.

## Mental model
DFS = recursion + visited set. Node visit karo, mark karo, har unvisited neighbor mein recurse karo, return. Yahi ek skeleton solve karta hai: connectivity, components, flood fill, path existence, cycle detection (directed: recursion-stack / 3-color se), aur post-order topological sort.

**Invariant:** `dfs(u)` return hone ke baad, `u` se reachable har node visited + marked hai. Visited node dobara enter karna no-op hai.

**Recursive vs iterative (Java):** Recursive default. Java mein `setrecursionlimit` nahi — deep graph pe `StackOverflowError` (thread stack ~10k–15k frames). Depth ~10⁴ se zyada ho sakti ho toh explicit `Deque<int[]>` stack ya big-stack thread.

## Questions
- LC 733 — Flood Fill (warm-up)
- LC 695 — Max Area of Island
- LC 841 — Keys and Rooms
- LC 130 — Surrounded Regions
- LC 133 — Clone Graph
