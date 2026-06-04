"""
This program implements Randomized Quicksort and Hashing with Chaining.

It also compares Randomized Quicksort with Deterministic Quicksort
on different types of input.

Deterministic Quicksort may fail on sorted or reverse-sorted input because
it always uses the first element as the pivot. The program catches that error
so it can keep running.
"""

import random
import time


# ============================================================
# PART 1: RANDOMIZED QUICKSORT
# ============================================================

def randomized_quicksort(arr):
    """
    Sorts a list using Randomized Quicksort.

    Randomized Quicksort works like normal Quicksort, except the pivot is chosen
    randomly from the current subarray.

    Choosing a random pivot helps avoid consistently bad pivot choices.

    Average-case time complexity:
        O(n log n)

    Worst-case time complexity:
        O(n^2)

    The worst case is still possible, but randomization makes it unlikely.
    """

    # Base case:
    # A list with 0 or 1 item is already sorted.
    if len(arr) <= 1:
        return arr

    # Choose a pivot uniformly at random.
    # Each element has the same chance of becoming the pivot.
    pivot = random.choice(arr)

    # Store values smaller than, equal to, and greater than the pivot.
    less = []
    equal = []
    greater = []

    # Partition the array into three parts.
    # The equal list helps handle repeated values efficiently.
    for value in arr:
        if value < pivot:
            less.append(value)
        elif value == pivot:
            equal.append(value)
        else:
            greater.append(value)

    # Recursively sort the less and greater parts.
    return randomized_quicksort(less) + equal + randomized_quicksort(greater)


def deterministic_quicksort(arr):
    """
    Sorts a list using Deterministic Quicksort.

    This version always chooses the first element as the pivot.

    This is useful for comparison because it performs badly on sorted and
    reverse-sorted arrays.

    Example:
        [1, 2, 3, 4, 5]

    Pivot = 1
    Left side = []
    Right side = [2, 3, 4, 5]

    This creates unbalanced partitions, which can lead to O(n^2) time.
    """

    # Base case.
    if len(arr) <= 1:
        return arr

    # Always choose the first element as the pivot.
    # This is intentionally simple but can be inefficient.
    pivot = arr[0]

    less = []
    equal = []
    greater = []

    # Partition the array.
    for value in arr:
        if value < pivot:
            less.append(value)
        elif value == pivot:
            equal.append(value)
        else:
            greater.append(value)

    return deterministic_quicksort(less) + equal + deterministic_quicksort(greater)


def generate_test_array(size, distribution):
    """
    Generates arrays with different input distributions, listed below:
    1. Random arrays
    2. Already sorted arrays
    3. Reverse-sorted arrays
    4. Arrays with repeated elements
    """

    if distribution == "random":
        return [random.randint(1, size) for _ in range(size)]

    elif distribution == "sorted":
        return list(range(size))

    elif distribution == "reverse":
        return list(range(size, 0, -1))

    elif distribution == "repeated":
        return [random.randint(1, 10) for _ in range(size)]

    else:
        raise ValueError("Unknown distribution type.")


def time_sorting_algorithm(sort_function, arr):
    """
    Measures how long a sorting function takes, and also safely handles RecursionError.

    Deterministic Quicksort can create very deep recursive calls when the input
    is already sorted or reverse sorted.

    Python has a maximum recursion depth. If that limit is exceeded, Python
    raises RecursionError. In such as case, it returns None.
    The comparison table will print "RecursionError" for that case.
    """

    # Copy the array so the original test input is not modified.
    arr_copy = arr.copy()

    start_time = time.perf_counter()

    try:
        # Run the sorting function.
        sorted_arr = sort_function(arr_copy)

    except RecursionError:
        # Return None to show that the algorithm failed due to deep recursion.
        return None

    end_time = time.perf_counter()

    # Optional correctness check:
    # This confirms that the algorithm actually sorted the array correctly.
    if sorted_arr != sorted(arr):
        raise ValueError(f"{sort_function.__name__} did not sort correctly.")

    return end_time - start_time


def compare_quicksort_algorithms():
    """
    Compares Randomized Quicksort and Deterministic Quicksort.

    Randomized Quicksort usually runs in O(n log n) time because
    the random pivot usually splits the array into smaller balanced parts.

    Deterministic Quicksort uses the first element as the pivot.
    This can be slow for sorted or reverse-sorted arrays because the pivot
    may create very uneven splits.
    """

    print("\n==============================")
    print("QUICKSORT EMPIRICAL COMPARISON")
    print("==============================")

    # Test sizes for the comparison.
    sizes = [100, 500, 900, 1200]

    # Different types of input arrays.
    distributions = ["random", "sorted", "reverse", "repeated"]

    for distribution in distributions:
        print(f"\nInput distribution: {distribution}")

        for size in sizes:
            # Create a test array for the current size and input type.
            arr = generate_test_array(size, distribution)

            # Measure how long each quicksort version takes.
            randomized_time = time_sorting_algorithm(randomized_quicksort, arr)
            deterministic_time = time_sorting_algorithm(deterministic_quicksort, arr)

            # Show RecursionError if randomized quicksort fails.
            if randomized_time is None:
                randomized_result = "RecursionError"
            else:
                randomized_result = f"{randomized_time:.6f} sec"

            # Show RecursionError if deterministic quicksort fails.
            if deterministic_time is None:
                deterministic_result = "RecursionError"
            else:
                deterministic_result = f"{deterministic_time:.6f} sec"

            # Print the timing results.
            print(
                f"Size: {size:5d} | "
                f"Randomized: {randomized_result:15s} | "
                f"Deterministic: {deterministic_result:15s}"
            )

    print("\nDiscussion:")
    print("- Randomized Quicksort usually performs well because it chooses a random pivot.")
    print("- Deterministic Quicksort can be slow when the array is already sorted or reverse sorted.")
    print("- A RecursionError means the algorithm made too many nested recursive calls.")
    print("- This shows the worst-case behavior of Deterministic Quicksort.")
    print("- Repeated values work well because equal values are grouped together.")


# ============================================================
# PART 2: HASHING WITH CHAINING
# ============================================================

class HashTableChaining:
    """
    Hash table using chaining.

    Chaining stores multiple key-value pairs in a list when they hash
    to the same table index.

    Load factor = number of items / number of slots.

    Expected time:
        Insert: O(1)
        Search: O(1 + alpha)
        Delete: O(1 + alpha)

    A lower load factor usually means fewer collisions and faster operations.
    """

    def __init__(self, initial_capacity=8):
        """
        Creates a new hash table with empty chains.
        """

        self.capacity = initial_capacity
        self.size = 0

        # Create empty chains for each table slot.
        self.table = [[] for _ in range(self.capacity)]

        # Prime number used by the hash function.
        self.prime = 109345121

        # Random values used to spread keys more evenly.
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

    def _hash(self, key):
        """
        Returns the table index for a key.
        """

        return ((self.a * hash(key) + self.b) % self.prime) % self.capacity

    def _load_factor(self):
        """
        Returns how full the table is.
        """

        return self.size / self.capacity

    def insert(self, key, value):
        """
        Adds or updates a key-value pair.
        """

        index = self._hash(key)
        chain = self.table[index]

        # Update the key if it already exists.
        for i, pair in enumerate(chain):
            existing_key, existing_value = pair

            if existing_key == key:
                # Replace the old value.
                chain[i] = (key, value)
                return

        # Add the new key-value pair.
        chain.append((key, value))
        self.size += 1

        # Resize when the table gets too full.
        if self._load_factor() > 0.75:
            self._resize()

    def search(self, key):
        """
        Finds and returns the value for a key.
        Returns None if the key is not found.
        """

        index = self._hash(key)
        chain = self.table[index]

        for existing_key, value in chain:
            if existing_key == key:
                return value

        return None

    def delete(self, key):
        """
        Removes a key-value pair if it exists.
        """

        index = self._hash(key)
        chain = self.table[index]

        for i, pair in enumerate(chain):
            existing_key, value = pair

            if existing_key == key:
                del chain[i]
                self.size -= 1
                return True

        return False

    def _resize(self):
        """
        Doubles the table size and rehashes all items.
        """

        old_table = self.table

        # Double the table capacity.
        self.capacity *= 2

        # Create a new empty table.
        self.table = [[] for _ in range(self.capacity)]

        # Reset size before adding items back.
        self.size = 0

        # Add all old items into the new table.
        for chain in old_table:
            for key, value in chain:
                self.insert(key, value)

    def display(self):
        """
        Prints the hash table contents.
        """

        print("\nHash Table Contents:")

        for index, chain in enumerate(self.table):
            print(f"Index {index}: {chain}")


def demonstrate_hash_table():
    """
    Shows how insert, search, update, and delete work.
    """

    print("\n==============================")
    print("HASH TABLE WITH CHAINING DEMO")
    print("==============================")

    hash_table = HashTableChaining()

    # Add key-value pairs.
    hash_table.insert("apple", 10)
    hash_table.insert("banana", 20)
    hash_table.insert("orange", 30)
    hash_table.insert("grape", 40)
    hash_table.insert("melon", 50)

    hash_table.display()

    # Search for keys.
    print("\nSearch Results:")
    print("apple:", hash_table.search("apple"))
    print("banana:", hash_table.search("banana"))
    print("unknown:", hash_table.search("unknown"))

    # Update an existing key.
    hash_table.insert("apple", 99)

    print("\nAfter updating apple:")
    print("apple:", hash_table.search("apple"))

    # Delete a key.
    print("\nDeleting banana...")
    deleted = hash_table.delete("banana")
    print("Deleted banana:", deleted)

    print("banana after deletion:", hash_table.search("banana"))

    hash_table.display()

    print("\nHash Table Analysis:")
    print("- Insert is expected O(1) when the load factor is low.")
    print("- Search is expected O(1 + alpha), where alpha is the load factor.")
    print("- Delete is expected O(1 + alpha).")
    print("- Dynamic resizing keeps the load factor low.")
    print("- A low load factor helps reduce collisions and keeps chains short.")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    """
    Main program that drives: 
        1. Randomized Quicksort
        2. Hashing with Chaining
    """

    compare_quicksort_algorithms()
    demonstrate_hash_table()


if __name__ == "__main__":
    main()