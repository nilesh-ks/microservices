# Pattern 2 — BFS (Breadth-First Search)

**One-liner:** Source(s) se WAVES mein process karo. Queue data structure hai. Unweighted (ya equal-weight) graph mein, node ko pehli baar reach karna = shortest path.

## Mental model
BFS = DFS ka level-by-level cousin. Visited ko **ENQUEUE pe** mark karo (dequeue pe nahi) taaki same node baar-baar push na ho. Distance track karo `int[]{node, dist}` enqueue karke, ya queue ko level-sized chunks (`int sz = q.size()`) mein process karke.

**Multi-source BFS:** "ANY source se har cell tak min distance" → saare sources ko **loop se pehle** dist 0 ke saath enqueue. Waves sab se ek saath failti hain — same O(V+E), no per-source restart.

**Invariant:** Jab node `u` pehli baar dequeue hota hai, `dist[u]` = closest source se minimum edges.

## Complexity note (BFS/DFS = O(V+E))
- Har vertex queue mein **ek baar** → O(V).
- Har vertex pe uske neighbors (edges) ek baar → Σ degree = O(E) (undirected: 2E).
- Total **O(V+E)**. Grid mein V=R·C, edges per cell ≤4 → E=O(R·C) → poora **O(R·C)**.
- Adjacency **list** se O(V+E); adjacency **matrix** se O(V²).

## Questions
- LC 1971 — Find if Path Exists in Graph (warm-up)
- LC 994 — Rotting Oranges (multi-source)
- LC 102 — Binary Tree Level Order Traversal
- LC 127 — Word Ladder
- LC 542 — 01 Matrix (multi-source)
