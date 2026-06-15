# LC 1971 — Find if Path Exists in Graph

**Pattern:** 2 — BFS (warm-up) · **Difficulty:** Easy · [LeetCode](https://leetcode.com/problems/find-if-path-exists-in-graph/)

**One-liner:** Sabse simple BFS — ek source, ek destination, sirf yes/no. Source se waves nikaalo, jaise hi destination dikhe `true`. Koi distance/level tracking nahi, koi grid coords nahi — bas **queue + visited + loop**.

## Mental model
Adjacency list banao (undirected → **dono directions**), source ko queue mein daalo, expand karo. Golden rule: **visited ENQUEUE pe mark karo** (dequeue pe nahi). Reachability = kya destination kabhi visit hua.

## Java (BFS)
```java
public boolean validPath(int n, int[][] edges, int source, int destination) {
    if (source == destination) return true;

    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] e : edges) {
        graph.get(e[0]).add(e[1]);          // undirected → dono taraf
        graph.get(e[1]).add(e[0]);
    }

    boolean[] visited = new boolean[n];
    Deque<Integer> q = new ArrayDeque<>();
    q.offer(source);
    visited[source] = true;                 // mark on ENQUEUE

    while (!q.isEmpty()) {
        int u = q.poll();
        if (u == destination) return true;
        for (int v : graph.get(u)) {
            if (!visited[v]) {
                visited[v] = true;
                q.offer(v);
            }
        }
    }
    return false;
}
```

## DFS version + ⚠️ recursion-depth
Constraints: `n`, `edges` dono **2·10⁵ tak**. Worst case ek lambi chain → recursive DFS depth ~2·10⁵ → Java `StackOverflowError`. Toh **iterative DFS / BFS safer**.

```java
// iterative DFS — recursion-safe (ArrayDeque as STACK: push/pop)
boolean[] visited = new boolean[n];
Deque<Integer> stack = new ArrayDeque<>();
stack.push(source); visited[source] = true;
while (!stack.isEmpty()) {
    int u = stack.pop();
    if (u == destination) return true;
    for (int v : graph.get(u))
        if (!visited[v]) { visited[v] = true; stack.push(v); }
}
return false;
```

## Stack vs Queue → dono ArrayDeque
Same class, alag access:
- **Queue (BFS, FIFO):** `offer` (tail) / `poll` (head)
- **Stack (DFS, LIFO):** `push` (head) / `pop` (head)

`ArrayDeque` dono ke liye best (faster than legacy `Stack`, `LinkedList`).

## Common traps
- **Undirected ko ek hi direction add karna** → aadhe paths miss.
- **Visited dequeue pe mark karna** → quadratic blow-up.
- **`source == destination`** edge case → `true`.
