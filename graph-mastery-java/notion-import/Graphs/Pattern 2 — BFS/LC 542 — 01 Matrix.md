# LC 542 — 01 Matrix

**Pattern:** 2 — BFS (multi-source) · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/01-matrix/)

**One-liner:** Har cell ke liye **nearest `0` tak distance**. Galti: har `1` se BFS (slow). Sahi: **saare `0`s ek saath source**, bahar ki taraf single BFS. Jab koi `1` pehli baar reach hota hai = uska nearest-zero distance.

## Mental model
Rotting Oranges (994) ka twin — "rot spreading" ki jagah "distance spreading." Problem **ulta** socho: "har 1 apna nearest 0 dhoonde" O((R·C)²); "saare 0 ek saath failein" O(R·C). Multi-source BFS guarantee — pehli baar wave jab cell tak pahunche, woh minimum distance (sab sources ek saath, equal speed).

## Java
```java
public int[][] updateMatrix(int[][] mat) {
    int R = mat.length, C = mat[0].length;
    int[][] dist = new int[R][C];
    Deque<int[]> q = new ArrayDeque<>();

    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (mat[r][c] == 0) { dist[r][c] = 0; q.offer(new int[]{r, c}); } // SAARE 0 sources
            else dist[r][c] = -1;                                            // unvisited marker
        }

    int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    while (!q.isEmpty()) {
        int[] cur = q.poll();
        int r = cur[0], c = cur[1];
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[r][c] + 1;   // parent dist + 1, mark on ENQUEUE
                q.offer(new int[]{nr, nc});
            }
        }
    }
    return dist;
}
```

## Why O((R·C)²) vs O(R·C)
- **Har `1` se alag BFS:** ~R·C searches × O(R·C) per search = **O((R·C)²)**. Paas-paas 1-cells overlapping area baar-baar scan karte hain (duplicate kaam).
- **Saare `0` se ek BFS:** har cell **ek baar** queue mein (visited mark), har cell O(1) → **O(R·C)**. Saara repeated scanning ek single sweep mein share.

## Common traps
- **Har `1` se BFS** → TLE. Ulta karo (0s = source).
- **`dist == 0` ko unvisited maan lena** — `0` valid source distance hai! Alag marker (`-1`) chahiye.
- **Visited dequeue pe mark** — neighbor ki dist enqueue ke time set.
- **`int[]{r,c}` kaafi** — dist `dist[][]` mein store, tuple mein nahi.

## DP alternative (bonus)
Do passes: top-left→bottom-right, phir bottom-right→top-left. O(R·C), no queue.
