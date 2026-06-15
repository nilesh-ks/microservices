# LC 127 — Word Ladder

**Pattern:** 2 — BFS · **Difficulty:** Hard · [LeetCode](https://leetcode.com/problems/word-ladder/)

**One-liner:** `beginWord` → `endWord`, ek baar mein ek letter, har intermediate `wordList` mein. Shortest transformation length = unweighted shortest path → **BFS**, aur **level count hi answer**. Neighbors **wildcard bucket map** se banao.

## Mental model
Har word node; edge jab ek letter ka farak. Naive (har pair compare) O(N²·L) → TLE. Smart: har word ke har position pe wildcard (`hit → "*it","h*t","hi*"`), map `pattern → [words]` precompute. Kisi word ke neighbors = uske L patterns ke buckets. O(N·L) edges. BFS level-by-level, jis level pe `endWord` mile wahi length.

## Java
```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> dict = new HashSet<>(wordList);
    if (!dict.contains(endWord)) return 0;

    int L = beginWord.length();
    Map<String, List<String>> buckets = new HashMap<>();
    for (String w : dict)
        for (int i = 0; i < L; i++) {
            String pattern = w.substring(0, i) + "*" + w.substring(i + 1);
            buckets.computeIfAbsent(pattern, k -> new ArrayList<>()).add(w);
        }

    Set<String> visited = new HashSet<>();
    Deque<String> q = new ArrayDeque<>();
    q.offer(beginWord);
    visited.add(beginWord);
    int level = 1;                                    // dono ends count → start 1

    while (!q.isEmpty()) {
        int sz = q.size();
        for (int k = 0; k < sz; k++) {
            String word = q.poll();
            if (word.equals(endWord)) return level;
            for (int i = 0; i < L; i++) {
                String pattern = word.substring(0, i) + "*" + word.substring(i + 1);
                for (String nei : buckets.getOrDefault(pattern, List.of())) {
                    if (!visited.contains(nei)) {
                        visited.add(nei);             // mark on ENQUEUE
                        q.offer(nei);
                    }
                }
            }
        }
        level++;
    }
    return 0;
}
```

## Common traps
- **Full adjacency O(N²·L)** → TLE. Wildcard bucket map → O(N·L).
- **Level off-by-one.** Answer mein begin + end dono count → `level = 1` se shuru.
- **`endWord` dict mein nahi** → turant `0`.
- **Visited dequeue pe mark.**
- **`beginWord` dict mein assume karna** — zaroori nahi.
- **Mutable shared empty list** mat do — `List.of()` / `Collections.emptyList()`.

## Optimization
**Bidirectional BFS** — dono ends se expand, milne pe ruko. `b^(d/2)+b^(d/2)` vs `b^d`.
