# LC 695 — Max Area of Island

**Pattern:** 1 — DFS · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/max-area-of-island/)

**One-liner:** Wahi Number of Islands wala flood-fill, bas ab DFS island ka **size (int) return** karta hai. Har source se area nikaalo, global max track karo.

## Mental model
LC 200 ka trivial extension. Har cell apne aap ko `1` count karta hai, phir apne 4 neighbors ke areas add karta hai. `dfs(r, c)` lautata hai "is cell se connected `1`s ka total count." Outer loop har naye unvisited `1` pe DFS chala kar `best` update karta hai.

## Java
```java
private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

public int maxAreaOfIsland(int[][] grid) {
    int R = grid.length, C = grid[0].length, best = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (grid[r][c] == 1)
                best = Math.max(best, dfs(grid, r, c, R, C));
    return best;
}

private int dfs(int[][] grid, int r, int c, int R, int C) {
    if (r < 0 || r >= R || c < 0 || c >= C) return 0;   // out of bounds → 0 area
    if (grid[r][c] != 1) return 0;                       // water / already counted → 0
    grid[r][c] = 0;                                      // sink (mark visited) BEFORE recursing
    int area = 1;                                        // current cell counts as 1
    for (int[] d : DIRS) area += dfs(grid, r + d[0], c + d[1], R, C);
    return area;
}
```

## Common traps
- **Recurse se pehle `grid[r][c] = 0` mark na karna.** Same cell baar-baar gina jayega → inflated area + stack blow-up. Mark pehle, phir 4 directions.
- **Current cell ka `1` add karna bhulna.** `area` ko `1` se start karo, `0` se nahi.
- **`void` DFS + bahar counter** chal jata hai, par `int` return karke `1 + sum(children)` cleaner — koi shared mutable state nahi.
- **`Math.max` se update karna bhoolna.** Har island ka area kaafi nahi; sabse bada answer hai.

## Difference from LC 200
200: DFS `void`, components **count**. 695: DFS **size return**, **max size** track. Skeleton same — sirf return type + accumulation badla.
