# Graphs

Java-first graph DSA prep — pattern-wise notes. Har pattern ka apna subpage, har subpage ke andar uske questions (mental model + Java code + traps + LeetCode link).

Derived from the "Graph Mastery" cheatsheet (9 patterns), translated to Java.

## Patterns
- **Pattern 1 — DFS** — connectivity, components, flood fill, cycle detection
- **Pattern 2 — BFS** — shortest path (unweighted), level order, multi-source

## Quick toolkit (Python → Java)
- `collections.deque` → `ArrayDeque<>` — queue: `offer`/`poll`, stack: `push`/`pop`
- `heapq` → `PriorityQueue<int[]>` (comparator; `Integer.compare` to avoid overflow)
- `defaultdict(list)` → `List<List<Integer>>` or `Map<..,List<..>>` + `computeIfAbsent`
- `float('inf')` → `Integer.MAX_VALUE` / `Long.MAX_VALUE` / sentinel `1_000_000_000`
- `sys.setrecursionlimit` → **no equivalent**; JVM throws `StackOverflowError` → go iterative or big-stack thread

## Status
- Pattern 1 (DFS): 733, 695, 841, 130, 133 ✅
- Pattern 2 (BFS): 1971, 994, 102, 127, 542 ✅
