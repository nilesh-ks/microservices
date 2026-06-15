# LC 733 — Flood Fill

**Pattern:** 1 — DFS (warm-up) · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/flood-fill/)

**One-liner:** Ek starting cell se DFS karke uske jaise original color wale saare 4-directionally connected cells ko `color` se repaint karo. No counting, no extra loop — bas "bounds check + color match + recurse 4 directions" rhythm.

## Mental model
Sabse simple flood fill — Number of Islands (LC 200) ka chhota bhai. Sirf ek source `(sr, sc)`, ek naya color, koi component-counting loop nahi. Visited tracking alag se nahi chahiye: cell ko `color` se paint karna hi "visited" mark hai (ab woh `start` color se match nahi karega).

## Java
```java
private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

public int[][] floodFill(int[][] image, int sr, int sc, int color) {
    int start = image[sr][sc];
    if (start != color) dfs(image, sr, sc, start, color);  // guard: infinite-loop se bachao
    return image;
}

private void dfs(int[][] img, int r, int c, int start, int color) {
    if (r < 0 || r >= img.length || c < 0 || c >= img[0].length) return;
    if (img[r][c] != start) return;        // galat color / already filled
    img[r][c] = color;                     // recurse karne se PEHLE mark karo
    for (int[] d : DIRS) dfs(img, r + d[0], c + d[1], start, color);
}
```

## Common traps
- **`start != color` guard bhulna.** Agar starting pixel ka color pehle se hi `color` ke barabar hai, paint karne par koi change nahi → `img[r][c] != start` kabhi true nahi → infinite recursion → `StackOverflowError`. Yeh #1 trap.
- **Recurse karne ke baad mark karna.** Same cell baar-baar push hoga. Hamesha `img[r][c] = color` pehle, phir recurse.
- **`start` ko inline mat lo.** `img[sr][sc]` ko variable mein store karo — source paint karte hi original color overwrite ho jata hai.

## Next
LC 733 → LC 200 (Number of Islands): wahi DFS skeleton + component-counting loop upar.
