# Graph Mastery — Java Edition

A Java-first rewrite of the "Graph Mastery" graph-algorithms cheatsheet (originally by
@rathoreadiitya, with all code in Python). Same 9 patterns, same decision tree, same 36-problem
set and 7-day plan — but **every template is idiomatic Java**, and every language-specific note
(recursion depth, heaps, hash maps, overflow guards) is written for the JVM instead of CPython.

## Contents

| File | What it is |
|---|---|
| `GraphMasteryJava.pdf` | The finished cheatsheet (read this). |
| `GraphMasteryJava.md` | Markdown source — edit this to change content. |
| `generate_pdf.py` | Renders the Markdown into the PDF. |

## What changed vs. the Python original

- All 11 code walkthroughs re-authored in Java (DFS, BFS, Topo/Kahn, DSU, Dijkstra,
  Bellman-Ford, Floyd-Warshall, Kruskal, grid BFS/DFS, bipartite).
- New **"Java toolkit"** section: a Python → Java cheat map (`deque`→`ArrayDeque`,
  `heapq`→`PriorityQueue`, `defaultdict`→`computeIfAbsent`, `float('inf')`→sentinels).
- Recursion-depth guidance rewritten for Java: there is no `sys.setrecursionlimit` — the JVM
  throws `StackOverflowError`, so the sheet shows the iterative-stack and big-stack-thread fixes.
- Java-specific traps added: comparator overflow (`a[0]-b[0]`), integer overflow when adding to
  an "infinity" sentinel, and `long` vs `1e9` sentinels in Bellman-Ford / Floyd-Warshall.

## Regenerate the PDF

```bash
pip install fpdf2          # needs DejaVu fonts (usually preinstalled on Linux)
python3 generate_pdf.py
```
