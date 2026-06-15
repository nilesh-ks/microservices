# LC 841 — Keys and Rooms

**Pattern:** 1 — DFS · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/keys-and-rooms/)

**One-liner:** Pattern 1 ka simplest **non-grid** DFS. Room `0` se shuru, har room mein kuch chaabiyaan (= dusre rooms ke numbers). DFS se saare reachable rooms mark karo, phir poocho: kya saare visit ho gaye?

## Mental model
Graph already adjacency list ke roop mein diya hai — `rooms.get(u)` hi `u` ke neighbors. Koi direction deltas / bounds check nahi; bas `boolean[] visited` aur seedha DFS. "for dr,dc in dirs" ki jagah "for key in rooms.get(u)". Answer = kya room `0` se saare nodes reachable.

## Java
```java
public boolean canVisitAllRooms(List<List<Integer>> rooms) {
    int n = rooms.size();
    boolean[] visited = new boolean[n];
    dfs(0, rooms, visited);                       // room 0 hamesha unlocked
    for (boolean v : visited) if (!v) return false;
    return true;
}

private void dfs(int u, List<List<Integer>> rooms, boolean[] visited) {
    visited[u] = true;                            // mark BEFORE recursing
    for (int key : rooms.get(u))
        if (!visited[key]) dfs(key, rooms, visited);
}
```

Count-based variant (visited scan ke bina):
```java
public boolean canVisitAllRooms(List<List<Integer>> rooms) {
    boolean[] visited = new boolean[rooms.size()];
    return dfs(0, rooms, visited) == rooms.size();
}
private int dfs(int u, List<List<Integer>> rooms, boolean[] visited) {
    visited[u] = true;
    int count = 1;
    for (int key : rooms.get(u))
        if (!visited[key]) count += dfs(key, rooms, visited);
    return count;
}
```

## Common traps
- **`visited[u] = true` recurse se pehle na karna.** Cycle (A→B, B→A) pe infinite recursion.
- **`!visited[key]` check bhulna.** Same room baar-baar enter hoga. Yeh check hi DFS terminate karta hai.
- **End condition:** answer tabhi `true` jab **saare** `n` rooms visited hon.
- **Grid-style sochna band karo.** Node IDs `0..n-1`, edges directly `rooms` list mein — pure graph DFS.

## Difference from 200/695
200/695 mein graph **implicit** (grid + deltas). Yahan graph **explicit adjacency list** — isliye "simplest non-grid DFS warm-up."
