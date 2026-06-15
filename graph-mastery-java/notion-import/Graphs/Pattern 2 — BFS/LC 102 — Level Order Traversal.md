# LC 102 — Binary Tree Level Order Traversal

**Pattern:** 2 — BFS · **Difficulty:** Medium · [LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/)

**One-liner:** Tree ko **level-by-level** BFS karo, har level ke values alag list mein. Trick: inner loop se pehle `q.size()` capture karo — utne nodes hi current level mein.

## Mental model
Tree bhi graph hai — bas cycles nahi, isliye `visited` ki zaroorat nahi. Queue ka current `size` = poora ek level. Us level ke saare nodes process karo, unke children next level ke liye enqueue, level ki list `res` mein push.

## Java
```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;

    Deque<TreeNode> q = new ArrayDeque<>();
    q.offer(root);

    while (!q.isEmpty()) {
        int sz = q.size();                       // is level ke nodes — LOOP SE PEHLE
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < sz; i++) {
            TreeNode node = q.poll();
            level.add(node.val);
            if (node.left  != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
        res.add(level);
    }
    return res;
}
```

## Common traps
- **`q.size()` ko loop condition mein likhna** (`i < q.size()`). Loop ke andar children add ho rahe → size badalta → levels mix. **Pehle `int sz` mein freeze karo.**
- **`null` children check bhulna** → `q.offer(null)` → aage NPE.
- **`root == null`** → empty list.
- **Tree mein `visited` lagana** — zaroorat nahi (no cycle).

## Variants (same skeleton)
- **Zigzag (LC 103):** har doosre level ki list reverse.
- **Right-side view (LC 199):** har level ka last element (`i == sz - 1`).

Ye "freeze level size, then drain" idiom min-rounds/levels wale problems mein kaam aata hai (994 minutes, 127 ladder length, parallel courses).
