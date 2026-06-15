# LC 994 — Rotting Oranges

**Pattern:** 2 — BFS (multi-source) · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/rotting-oranges/)

**One-liner:** Saare **rotten oranges ko ek saath source** banao (time 0), phir BFS. Har wave = 1 minute. Answer = last wave ka time. Koi fresh bacha → `-1`.

## Mental model
`0`=empty, `1`=fresh, `2`=rotten. Galti: har rotten se alag BFS. Sahi: **multi-source BFS** — shuru mein hi *saare* rotten oranges queue mein (sabka time 0). Ek `fresh` counter; jab fresh rot karo, `fresh--`. Last orange jis minute rota = answer.

## Java
```java
public int orangesRotting(int[][] grid) {
    int R = grid.length, C = grid[0].length, fresh = 0;
    Deque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] == 2) q.offer(new int[]{r, c, 0});  // SAARE sources pehle
            else if (grid[r][c] == 1) fresh++;
        }
    int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int time = 0;
    while (!q.isEmpty()) {
        int[] cur = q.poll();
        int r = cur[0], c = cur[1], t = cur[2];
        time = t;
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && grid[nr][nc] == 1) {
                grid[nr][nc] = 2;          // mark on ENQUEUE
                fresh--;
                q.offer(new int[]{nr, nc, t + 1});
            }
        }
    }
    return fresh == 0 ? time : -1;
}
```

## Common traps
- **Sources ek-ek karke loop ke andar enqueue.** Saare rotten **while se PEHLE** daalo.
- **`fresh` count na rakhna** → unreachable fresh detect nahi hoga → `-1` miss.
- **Visited dequeue pe mark** → wahi `2` banana enqueue ke time karo.
- **Empty queue:** koi rotten/fresh nahi → `0`. Code handle karta hai.

## Level-by-level alternative
```java
while (!q.isEmpty() && fresh > 0) {
    int sz = q.size();
    for (int i = 0; i < sz; i++) { /* ...rot neighbors, fresh--... */ }
    minutes++;
}
return fresh == 0 ? minutes : -1;
```
Dono O(R·C). `int[]{r,c,t}` compact; level-chunk "har iteration = 1 minute" explicit.

## Twin: LC 542
994 = single number (last minute); 542 = poora distance grid. Dono multi-source BFS.
