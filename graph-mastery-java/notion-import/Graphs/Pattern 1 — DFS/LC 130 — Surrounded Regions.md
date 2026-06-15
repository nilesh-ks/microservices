# LC 130 — Surrounded Regions

**Pattern:** 1 — DFS · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/surrounded-regions/)

**One-liner:** Direct mat poocho "kaunse `'O'` trapped hain" — ulta poocho "kaunse `'O'` border tak pahunchte hain." Border se DFS karke survivors mark karo, baaki sab `'O'` trapped → `'X'`.

## Mental model
Pattern 1 ka signature **boundary-expansion** trick. Koi bhi `'O'` jo border se connected hai woh capture nahi ho sakta. Toh seedha "trapped" detect karne ki jagah, har border `'O'` se DFS chalao aur poore connected region ko temporary marker `'#'` se mark karo. Phir final sweep:
- bacha hua `'O'` = trapped → `'X'`
- `'#'` = survivor → wapas `'O'`

## Java
```java
private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

public void solve(char[][] board) {
    if (board == null || board.length == 0) return;
    int R = board.length, C = board[0].length;

    for (int r = 0; r < R; r++) {                // left/right borders
        dfs(board, r, 0, R, C);
        dfs(board, r, C - 1, R, C);
    }
    for (int c = 0; c < C; c++) {                // top/bottom borders
        dfs(board, 0, c, R, C);
        dfs(board, R - 1, c, R, C);
    }

    for (int r = 0; r < R; r++)                  // flip
        for (int c = 0; c < C; c++) {
            if (board[r][c] == 'O') board[r][c] = 'X';        // trapped
            else if (board[r][c] == '#') board[r][c] = 'O';   // survivor
        }
}

private void dfs(char[][] b, int r, int c, int R, int C) {
    if (r < 0 || r >= R || c < 0 || c >= C) return;
    if (b[r][c] != 'O') return;                  // sirf 'O' expand ('X'/'#' skip)
    b[r][c] = '#';                               // survivor mark, recurse se PEHLE
    for (int[] d : DIRS) dfs(b, r + d[0], c + d[1], R, C);
}
```

## Kyun "saare 0 → #" nahi hote (common doubt)
DFS sirf **border se** start hoti hai, aur `'X'` ek **deewar** hai (`if (b[r][c] != 'O') return;`). Trapped region poori tarah `'X'` se ghira hota hai, toh border se flood wahan pahunch hi nahi sakti → woh `'O'` hi rehte hain → final sweep mein `'X'` ban jaate hain. Har recursive call dobara guard check karti hai, isliye sirf ek connected border-region fill hota hai.

## Common traps
- **Trapped regions directly find karna** (messy, har region pe flag carry karna). Reverse (border → andar) clean hai.
- **Temporary marker `'#'` na use karna** → final sweep mein survivor vs trapped `'O'` distinguish nahi honge.
- **Final flip mein dono conversions** (`'O'→'X'` aur `'#'→'O'`) zaroori.
- **In-place / `void`** — extra `visited[][]` ki zaroorat nahi.

## Connection
Wahi boundary-expansion Pattern 8 ke LC 417 Pacific Atlantic mein dobara.
