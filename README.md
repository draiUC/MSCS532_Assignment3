# MSCS532 Assignment 3: Algorithm Efficiency and Scalability

## Overview

This project implements and empirically compares two fundamental algorithms:

1. **Randomized Quicksort** — a sorting algorithm that selects a pivot uniformly at random to achieve O(n log n) average-case performance.
2. **Hashing with Chaining** — a hash table that resolves collisions by storing multiple key-value pairs in linked chains, supporting O(1) expected insert, search, and delete.

---

## Files

```
algo.py   — Main Python source file containing all implementations 
README.md 
```

---

## Requirements

- Python 3.8 or higher
- No external dependencies 

---

## How to Run

```bash
python algo.py
```

This runs both parts of the assignment sequentially and prints all output to the terminal.

---

## Part 1: Randomized Quicksort

### Implementation

`randomized_quicksort(arr)` selects a pivot uniformly at random from the current subarray, then partitions elements into three groups — less than, equal to, and greater than the pivot — and recurses on the outer two groups.

`deterministic_quicksort(arr)` always uses the first element as the pivot, which is intentionally naïve and serves as a performance baseline.

### Empirical Comparison

The program tests both algorithms on four input distributions across four sizes (100, 500, 900, 1200):

| Distribution | Description |
|---|---|
| `random` | Uniformly random integers |
| `sorted` | Already sorted in ascending order |
| `reverse` | Sorted in descending order |
| `repeated` | Values drawn from a small range (1–10) |

### Sample Output

```
==============================
QUICKSORT EMPIRICAL COMPARISON
==============================

Input distribution: random
Size:   100 | Randomized: 0.000322 sec  | Deterministic: 0.000080 sec
Size:   500 | Randomized: 0.000594 sec  | Deterministic: 0.000542 sec
Size:   900 | Randomized: 0.001122 sec  | Deterministic: 0.001270 sec
Size:  1200 | Randomized: 0.002809 sec  | Deterministic: 0.001800 sec

Input distribution: sorted
Size:   100 | Randomized: 0.000116 sec  | Deterministic: 0.000491 sec
Size:   500 | Randomized: 0.000632 sec  | Deterministic: 0.012090 sec
Size:   900 | Randomized: 0.001003 sec  | Deterministic: 0.039088 sec
Size:  1200 | Randomized: 0.001418 sec  | Deterministic: RecursionError

Input distribution: reverse
Size:   100 | Randomized: 0.000094 sec  | Deterministic: 0.000501 sec
Size:   500 | Randomized: 0.000732 sec  | Deterministic: 0.007037 sec
Size:   900 | Randomized: 0.002375 sec  | Deterministic: 0.026555 sec
Size:  1200 | Randomized: 0.001469 sec  | Deterministic: RecursionError

Input distribution: repeated
Size:   100 | Randomized: 0.000035 sec  | Deterministic: 0.000033 sec
Size:   500 | Randomized: 0.000125 sec  | Deterministic: 0.000099 sec
Size:   900 | Randomized: 0.000194 sec  | Deterministic: 0.000179 sec
Size:  1200 | Randomized: 0.000243 sec  | Deterministic: 0.000300 sec
```

### Key Observations

- On **sorted** and **reverse-sorted** inputs, Deterministic Quicksort degrades severely and triggers a `RecursionError` at size 1200 due to O(n²) recursion depth.
- Randomized Quicksort performs consistently well across all distributions.
- On **repeated** values, both algorithms perform similarly because equal elements are grouped together, limiting recursion depth.

---

## Part 2: Hashing with Chaining

### Implementation

`HashTableChaining` implements a hash table with the following properties:

- **Hash function:** Universal hashing using parameters `a`, `b`, and a large prime, providing strong distribution guarantees.
- **Collision resolution:** Chaining — each slot holds a list of `(key, value)` pairs.
- **Dynamic resizing:** The table doubles in capacity when the load factor exceeds 0.75, rehashing all existing entries.

### Supported Operations

| Operation | Expected Time Complexity |
|---|---|
| `insert(key, value)` | O(1) amortized |
| `search(key)` | O(1 + α) |
| `delete(key)` | O(1 + α) |

Where α = n/m is the load factor (n = number of elements, m = number of slots).

### Sample Output

```
==============================
HASH TABLE WITH CHAINING DEMO
==============================

Hash Table Contents:
Index 0: [('apple', 10), ('orange', 30)]
Index 1: []
Index 2: [('banana', 20), ('melon', 50)]
Index 3: []
Index 4: []
Index 5: [('grape', 40)]
Index 6: []
Index 7: []

Search Results:
apple: 10
banana: 20
unknown: None

After updating apple:
apple: 99

Deleting banana...
Deleted banana: True
banana after deletion: None
```

### Key Properties

- Inserting a key that already exists **updates** the value rather than creating a duplicate.
- Searching for a missing key returns `None`.
- Dynamic resizing keeps the load factor below 0.75, ensuring short chains and fast operations.

---

## Complexity Summary

| Algorithm / Operation | Average Case | Worst Case |
|---|---|---|
| Randomized Quicksort | O(n log n) | O(n²) |
| Deterministic Quicksort | O(n log n) | O(n²) |
| Hash Insert | O(1) | O(n) |
| Hash Search | O(1 + α) | O(n) |
| Hash Delete | O(1 + α) | O(n) |

---

## Observation

**Randomized Quicksort outperforms Deterministic Quicksort on sorted/reverse-sorted input**

Deterministic Quicksort always picks the first element as pivot. On sorted or reverse-sorted arrays, this produces maximally unbalanced partitions of size 0 and n−1 at every level, resulting in O(n²) time and O(n) recursion depth. Python's recursion limit (~1000) causes a `RecursionError` at n=1200.

Randomized Quicksort picks pivots uniformly at random, making catastrophically unbalanced partitions exponentially unlikely. The expected number of comparisons is O(n log n) regardless of input order.

**Hashing with Chaining is efficient**

With a good hash function and a load factor α kept below a constant threshold, each chain has expected length α. Insert, search, and delete each require O(1) hash computation plus O(α) chain traversal — giving O(1 + α) = O(1) expected time. Dynamic resizing ensures α stays bounded.