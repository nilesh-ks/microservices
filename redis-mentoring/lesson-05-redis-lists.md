# Lesson 5 — Redis Lists

> Level 2 (Redis Data Structures). Mentoring notes — detailed enough to revise without the original conversation.
> Teaching style: Hinglish, WHY before HOW, mental models first.

---

## Recap of Lesson 4 (Strings) — carried forward

- **String = binary-safe byte array** (not just text). Stores text, JSON, serialized objects, image bytes. Max size **512 MB**.
- `SET` / `GET` / `DEL` = basic CRUD.
- `INCR` / `INCRBY` / `DECR` / `DECRBY` = atomic integer ops on a string holding a number.
- **Atomicity** comes from Redis being **single-threaded** — no race conditions, no explicit locks needed.
- Counters: `INCR` + `EXPIRE` = fixed/sliding window counter foundation (page views, rate limits, likes).
- `SETNX` and `SET key val NX EX 30` = distributed lock foundation. `NX` = set only if key absent. `EX` = expiry seconds.
- String limitation: storing JSON forces a **read-modify-write** cycle (GET → deserialize → modify → serialize → SET) to update a single field → race conditions + network overhead. Structured data → use Hash instead.

### Understanding-check questions (with answers)
1. **Why is `INCR` atomic without a lock?** Redis executes commands on a single thread, one at a time. No two commands interleave, so read-add-write happens as one indivisible step.
2. **Why is JSON-in-a-String bad for partial updates?** You must fetch the whole blob, deserialize, change one field, reserialize, and write it all back — expensive and race-prone under concurrency.
3. **What do `NX` and `EX` guarantee separately?** `NX` = only set if the key does not already exist (mutual exclusion). `EX` = auto-expire after N seconds (so a crashed lock holder doesn't deadlock forever). Together in one atomic command they form a safe lock.

---

## 1. What is it?
Redis List = an **ordered collection of strings**, stored in insertion order. Internally a **linked list** (optimized), not an array.
- Insert/remove at **both ends (head & tail) = O(1)**.
- Access in the **middle by index = O(N)**.
- Allows **duplicates**, preserves **order**.
- Mental analogy: Java `LinkedList<String>`, but in-memory on a Redis server.

```
HEAD                                    TAIL
 ↓                                        ↓
[ "job1" ] -> [ "job2" ] -> [ "job3" ] -> [ "job4" ]
 left/front                            right/back
```

## 2. Why does it exist?
Strings hold a single value. Backends frequently need an **ordered sequence of items under one key** where order matters (message queue, recent activity feed, notifications). Without Lists you'd scatter items across keys (`task:1`, `task:2`…) and manage order with a manual counter — messy, non-atomic, error-prone.

## 3. What problem does it solve?
- **A) Ordered data** without manual indexing.
- **B) Queue (FIFO) / Stack (LIFO) semantics** out of the box.
- **C) Producer–Consumer decoupling** — producer pushes work, consumer pops it; neither must be online simultaneously. List = buffer. Foundation of **async processing**.

> Redis List + blocking pop = lightweight, fast job queue. Common at small/medium scale before adopting Kafka/RabbitMQ.

## 4. Internal mental model (most important)

### Model #1 — Deque (double-ended queue)
Command prefixes:
- `L` = **Left** = head = front
- `R` = **Right** = tail = back

So `LPUSH`/`RPUSH` push at head/tail; `LPOP`/`RPOP` remove at head/tail. Learn this once → all 20+ list commands become intuitive.

### Model #2 — Indexing from both ends (Python-like)
- Positive index from front: `0`=first, `1`=second…
- Negative index from end: `-1`=last, `-2`=second-last…
- `LRANGE key 0 -1` = entire list.

### Model #3 — Internal encoding (the deep part)
**Old Redis (<3.2):** two encodings —
- `ziplist` — small lists, one contiguous memory block (array-like, memory-efficient) but middle insertion shifts memory → O(N).
- `linkedlist` — large lists, classic doubly linked list; **2 pointers (~16 bytes) overhead per element** → wasteful for small values, poor cache locality.

**New Redis (3.2+): `quicklist`** (default today).
- A **doubly linked list of ziplists** (ziplist replaced by `listpack` in Redis 7.0+).
```
quicklist node -> [listpack: a,b,c,d] <-> [listpack: e,f,g,h] <-> [listpack: i,j]
```
- **Best of both worlds:** O(1) push/pop at ends (linked-list property) + memory efficiency & cache locality (packed blocks, no per-element pointer overhead).
- Elements per node controlled by `list-max-listpack-size` (old name `list-max-ziplist-size`).

> **Interview gold:** "Redis List is a quicklist — a doubly linked list of listpacks/ziplists. Not a pure linked list (pointer overhead + bad cache locality) and not a pure array (need O(1) end inserts). Quicklist is the hybrid."

## 5. Commands & syntax (grouped)

**A) Push**
```
LPUSH key value [value ...]   # head
RPUSH key value [value ...]   # tail
LPUSHX key value              # push only if key already exists
RPUSHX key value
```
Note: `LPUSH mylist a b c` pushes a, then b, then c one-by-one → result `[c, b, a]`.

**B) Pop**
```
LPOP key [count]              # remove+return from head
RPOP key [count]              # remove+return from tail   (count is Redis 6.2+)
```

**C) Read (peek)**
```
LRANGE key start stop         # range, both ends inclusive
LINDEX key index              # element at index
LLEN key                      # length
```
`LRANGE key 0 -1` = whole list.

**D) Modify**
```
LSET key index value                  # replace element at index
LINSERT key BEFORE|AFTER pivot value  # insert relative to an existing element
LREM key count value                  # remove matching elements
LTRIM key start stop                  # keep only the range, delete the rest
```

**E) Blocking (queue heart)**
```
BLPOP key [key ...] timeout   # blocking head pop
BRPOP key [key ...] timeout   # blocking tail pop
```

**F) Move between lists (reliable queue)**
```
RPOPLPUSH source destination               # deprecated 6.2+
LMOVE source dest LEFT|RIGHT LEFT|RIGHT     # flexible, atomic
BLMOVE source dest LEFT|RIGHT LEFT|RIGHT timeout  # blocking version
```

## 6. Command component breakdown
- **`LPUSH queue "job1"`** — `LPUSH`=op (head insert); `queue`=key (auto-created if absent); `"job1"`=value.
- **`LRANGE queue 0 -1`** — `0`=start (inclusive), `-1`=last (inclusive) → whole list.
- **`LTRIM queue 0 99`** — keep indices 0..99 (first 100), delete the rest → capped list.
- **`LREM queue 2 "job1"`** — `count` sign matters: `>0` head→tail remove first `count` matches; `<0` tail→head remove first `|count|`; `=0` remove **all** matches.
- **`BLPOP queue 5`** — block up to `5`s; `0` = block forever; returns `nil` on timeout. Can pass multiple keys.
- **`LMOVE source dest LEFT RIGHT`** — pop from source head, push to dest tail, **atomically**. Core of reliable-queue pattern.

## 7. Time complexity
| Command | Complexity | Why |
|---|---|---|
| `LPUSH`/`RPUSH` | O(1) per element | only head/tail pointer update |
| `LPOP`/`RPOP` | O(1) (O(N) with count) | remove at end |
| `LLEN` | O(1) | length cached |
| `LINDEX` | O(N) | must walk to index |
| `LSET` | O(N) | walk to index |
| `LINSERT` | O(N) | find pivot |
| `LRANGE` | O(S+N) | S=offset to start, N=returned |
| `LREM` | O(N) | scan list |
| `LTRIM` | O(N) | N=removed |
| `BLPOP`/`BRPOP` | O(1) | pop, but blocks |

> **Golden rule:** *Ends = O(1), middle = O(N).* Never use Lists for random access by index.

## 8. Real-world usage

### Job queue (FIFO)
```
# Producer
RPUSH order:queue "{orderId:1023, action:'send_email'}"
# Consumer
BLPOP order:queue 0     # blocks until a job arrives
```
`RPUSH` tail + `BLPOP` head = FIFO. `BLPOP 0` avoids busy-wait.

Java (Jedis, detail in Level 3):
```java
// Producer
jedis.rpush("order:queue", objectMapper.writeValueAsString(order));

// Consumer worker
while (true) {
    List<String> result = jedis.blpop(0, "order:queue"); // [key, value], 0=block forever
    Order order = objectMapper.readValue(result.get(1), Order.class);
    process(order);
}
```

### Recent activity feed (capped list)
```
LPUSH user:1023:activity "logged_in"
LTRIM user:1023:activity 0 49      # keep latest 50
LRANGE user:1023:activity 0 9      # show latest 10
```
`LPUSH` keeps newest at head; `LTRIM` prevents unbounded growth. Pattern = **capped collection**.

### Reliable queue (LMOVE pattern)
Problem with plain `BLPOP`: if worker crashes **after** popping but **before** finishing, the job is lost (at-most-once).
Fix:
```
LMOVE order:queue order:processing LEFT RIGHT   # atomically move to processing
# ... process ...
LREM order:processing 1 "<job>"                 # remove after success
```
Crash → job survives in `order:processing` → recoverable. Gives **at-least-once** delivery. Production-grade queues use this.

## 9. Production pitfalls
1. **Unbounded growth (memory bomb):** fast producer + slow/down consumer → RAM fills, evictions/write failures. Always cap (`LTRIM`), monitor (`LLEN`), or apply backpressure.
2. **Treating LINDEX/LSET as array access:** looping `LINDEX` per index = O(N²). Use one `LRANGE 0 -1` instead.
3. **Big keys:** millions of elements in one list → `LRANGE 0 -1` blocks the single-threaded event loop → latency spike for ALL clients. `DEL` of big key is O(N) + blocking — use `UNLINK` (async). In Cluster, one key lives on one shard → hot/big list unbalances the cluster.
4. **Lost jobs with plain BLPOP:** crash loses the job. Use reliable-queue (LMOVE) for critical work.
5. **Blocking commands + connection pooling:** `BLPOP 0` holds a connection until data arrives. With a shared pool (typical in Java), use a **dedicated connection** for blocking ops or the pool starves. (Detail in Level 3.)
6. **Fan-out need:** plain List delivers each element to exactly one consumer (pop is atomic) — good for work distribution, wrong for broadcast. For fan-out use Pub/Sub or Streams (consumer groups).

## 10. Interview discussion points
- **Internal storage?** Quicklist = doubly linked list of listpacks/ziplists; hybrid for O(1) ends + memory efficiency + cache locality.
- **List vs Kafka/RabbitMQ?** Redis List: simple, fast, low-latency, low-ops, small/medium scale; but no built-in consumer groups (plain list), no replay/partitioning, weaker durability (RDB/AOF dependent). Kafka: durable log, replay, partitioning, consumer groups, high throughput, but heavy ops + higher latency. **Redis Streams** = middle ground (consumer groups + persistence). Stating this trade-off is a strong signal.
- **FIFO vs LIFO?** FIFO: `RPUSH`+`LPOP` (or `LPUSH`+`RPOP`). LIFO/stack: `LPUSH`+`LPOP` (same end).
- **Crash-safe queue?** `LMOVE`/`BRPOPLPUSH` to a processing list, `LREM` after success → at-least-once; recovery requeues stuck jobs.
- **BLPOP vs busy-wait?** BLPOP blocks on Redis and is woken when data arrives — no wasted CPU/round-trips, unlike `while(LLEN==0)`.
- **Is `LRANGE 0 -1` safe in prod?** Depends on size; large lists block the single thread. Use pagination/capping.

## 11. Summary
- List = ordered string collection; internally **quicklist** (linked list of listpacks).
- **Ends O(1)**, **middle O(N)**. `L`=head, `R`=tail.
- Build **FIFO** and **LIFO** trivially.
- `BLPOP`/`BRPOP` = efficient blocking consumer.
- `LMOVE`/`BRPOPLPUSH` = reliable, crash-safe queue (at-least-once).
- `LTRIM` = capped list (bound memory).
- Pitfalls: unbounded growth, big keys blocking single thread, lost jobs, blocking-command pool exhaustion.
- Need fan-out → Streams/Pub-Sub, not Lists.

## 12. Notes / open threads for later
- Deeper dive on `BLPOP` connection handling → **Level 3 (Jedis/Lettuce, connection pooling, thread safety)**.
- Single-threaded event loop & why big-key commands cause global latency → **Level 4 (Internals)**.
- Streams + consumer groups (fan-out, replay, acks) → **Level 2 (Streams lesson)** and contrasted again in **Level 5**.
- Reliable-queue recovery (requeue stuck jobs from processing list) → revisit in **Level 5 (Production patterns)**.

---
**Next lesson:** Redis Sets.
