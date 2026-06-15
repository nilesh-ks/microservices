# LC 133 — Clone Graph

**Pattern:** 1 — DFS · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/clone-graph/)

**One-liner:** Connected undirected graph ka **deep copy**. Ek `HashMap<Node, Node>` rakho jo "original node → clone" map kare. DFS karte jao; visited-tracking + duplicate-avoidance dono yahi map handle karta hai.

## Mental model
"Visited set" ki jagah ek **visited map** — `clones` do kaam karta hai: (1) node already copy hua ya nahi (cycle se bachne ke liye), (2) us node ka clone reference (neighbors wire karne ke liye). Skeleton wahi DFS, bas `boolean[] visited` → `Map<Node,Node>`. Critical: **clone ko map mein recurse se PEHLE daalo** — warna cycle (A↔B) mein infinite recursion.

## Java
```java
// class Node { int val; List<Node> neighbors; ... }

public Node cloneGraph(Node node) {
    if (node == null) return null;
    return dfs(node, new HashMap<>());
}

private Node dfs(Node node, Map<Node, Node> clones) {
    if (clones.containsKey(node)) return clones.get(node);   // pehle se copy → wahi lautao

    Node copy = new Node(node.val);
    clones.put(node, copy);              // map mein daalo RECURSE se PEHLE (cycle-safe)

    for (Node nei : node.neighbors)
        copy.neighbors.add(dfs(nei, clones));   // har neighbor ka clone wire karo

    return copy;
}
```

## Common traps
- **Clone ko map mein recurse ke baad daalna.** Cycle (A↔B) pe infinite recursion → `StackOverflowError`. Naya clone banate hi turant register karo.
- **`containsKey` check bhulna.** Yahi "visited" hai; iske bina har edge dobara naya clone banayega.
- **`neighbors` wire karna bhoolna.** Deep copy = naye clone ke `neighbors` mein **clones** daalo, originals nahi.
- **`node == null` edge case.** Empty graph → `null`.
- **BFS variant** (queue + same map) bhi chalega; deep graph pe iterative `StackOverflowError` se bachata hai.

## Difference from baaki Pattern-1
200/695/841 mein sirf visit/count (`boolean[]` kaafi). Yahan har visited node ka **naya object yaad** rakhna hai (edges re-wire ke liye) — isliye `Set` → `Map<Node,Node>`. "Deep-copy a graph" ka canonical.
