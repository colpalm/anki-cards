# Python Fundamentals Anki Cards

## Sources
- [NeetCode Python for Beginners](https://neetcode.io/problems/python-hello-world/question)
- [NeetCode Python for Coding Interviews](https://neetcode.io/problems/python-sort-ascending/question)


## Cards

### Floor Division with Negatives
**Front:**
What is the result of `-7 // 2` in Python? Why?

**Back:**
`-4`

Floor division rounds *down* (toward negative infinity), not toward zero.
- `-7 / 2 = -3.5`
- Rounding down gives `-4`

Contrast with integer division in C/Java which truncates toward zero (would give `-3`).

---

### Boolean Operator Precedence
**Front:**
What is the order of precedence for Python's boolean operators `not`, `and`, `or`?

**Back:**
`not` → `and` → `or` (highest to lowest)

Example:
```python
not True or True and False
# Evaluates as: ((not True) or (True and False))
# = (False or False)
# = False
```

Use parentheses to make intent clear.

---

### Falsy Values
**Front:**
List all the falsy values in Python.

**Back:**
- `False`
- `None`
- `0` (int)
- `0.0` (float)
- `""` (empty string)
- `[]` (empty list)
- `{}` (empty dict)
- `set()` (empty set)
- `()` (empty tuple)

Pythonic: `if my_list:` instead of `if len(my_list) > 0:`

---

### Mutable Default Argument Pitfall
**Front:**
What's wrong with this code?
```python
def append_to(item, lst=[]):
    lst.append(item)
    return lst
```

**Back:**
The default list `[]` is created **once** at function definition, not on each call. All calls share the same list object.

```python
append_to(1)  # [1]
append_to(2)  # [1, 2] — not [2]!
```

**Fix:** Use `None` as default:
```python
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

### String Reversal with Slicing
**Front:**
How do you reverse a string in Python using slicing? Explain why it works.

**Back:**
```python
s[::-1]
```

Slicing syntax: `s[start:end:step]`
- Omitted `start`: beginning of string
- Omitted `end`: end of string
- `step = -1`: traverse backward

```python
"hello"[::-1]  # "olleh"
```

---

### Negative Indexing
**Front:**
Given `lst = [10, 20, 30, 40, 50]`, what do these return?
- `lst[-1]`
- `lst[-2]`
- `lst[-3:]`

**Back:**
- `lst[-1]` → `50` (last element)
- `lst[-2]` → `40` (second to last)
- `lst[-3:]` → `[30, 40, 50]` (last three elements)

Negative indices count backward from the end, starting at `-1`.

---

### Dictionary .get() Method
**Front:**
What's the difference between `d[key]` and `d.get(key, default)`?

**Back:**
`d[key]`: Raises `KeyError` if key doesn't exist.

`d.get(key, default)`: Returns `default` if key doesn't exist (no error). If `default` is omitted, returns `None`.

```python
d = {"a": 1}
d["b"]           # KeyError
d.get("b", 0)    # 0
d.get("b")       # None
```

Useful for counting:
```python
freq[x] = freq.get(x, 0) + 1
```

---

### Empty Set Creation
**Front:**
How do you create an empty set in Python? What does `{}` create?

**Back:**
```python
empty_set = set()    # empty set
empty_dict = {}      # empty dict (NOT a set!)
```

`{}` creates an empty **dictionary**, not a set.

Non-empty sets use braces: `{1, 2, 3}`

```python
type({})      # <class 'dict'>
type(set())   # <class 'set'>
type({1})     # <class 'set'>
```

---

### Generator Expression vs List Comprehension
**Front:**
What's the difference between these two? When would you use one over the other?
```python
sum([x * x for x in range(1000000)])
sum(x * x for x in range(1000000))
```

**Back:**
First: **List comprehension** — creates entire list in memory, then passes to `sum()`.

Second: **Generator expression** — yields values one at a time, never storing the full list.

```python
[x * x for x in range(1000000)]  # Allocates ~8MB for the list
(x * x for x in range(1000000))  # Allocates almost nothing
```

**Use generator expressions when:**
- Passing directly to a function that consumes iterables (`sum`, `max`, `min`, `''.join()`)
- Processing large/infinite sequences
- You only need to iterate once

**Use list comprehensions when:**
- You need to index into results or iterate multiple times
- You need `len()` or other list methods

---

### Different Error Types
**Front:**
Describe the three types of errors:
- **Syntax Error**
- **Runtime Error**
- **Logical Error**

**Back:**
- **Syntax errors** occur when the code is not written correctly according to the rules of the programming language. It's not so different from a spelling or grammar error in a human language, except that computers are much less forgiving. e.g. a missing quote or parenthesis
- A **runtime error** is an error that occurs while the program is running. That means the syntax of the program itself is fine. It is usually caused by something that the programmer did not anticipate. Runtime errors can be difficult to debug because they may not always occur consistently. For example, if we programmed a calculator and the user tries to divide by zero, we will get a runtime error.
- A **logical error** is an error that occurs when the program runs without crashing or producing an error, but the output is not what the programmer intended. This is commonly known as a bug. Logical errors can be difficult to find because as programmers we have to identify which lines of code are causing the incorrect output. There are various techniques to debug logical errors, but in large programs, it can still be very challenging.

---

### .sort() vs sorted()
**Front:**
What's the difference between `list.sort()` and `sorted(list)`?

**Back:**
`.sort()`: Sorts **in-place**, returns `None`
- Modifies the original list
- Space: O(1)

`sorted()`: Returns a **new sorted list**
- Original list unchanged
- Space: O(n)

```python
nums = [3, 1, 2]
nums.sort()        # nums is now [1, 2, 3], returns None

nums = [3, 1, 2]
result = sorted(nums)  # result is [1, 2, 3], nums unchanged
```

Both have O(n log n) time complexity (Timsort).

---

### Reverse Sorting
**Front:**
How do you sort a list in descending order in Python? Show two approaches.

**Back:**
**Option 1:** Use `reverse=True` parameter
```python
nums = [3, 1, 2]
nums.sort(reverse=True)  # [3, 2, 1]

# Or with sorted()
sorted(nums, reverse=True)  # [3, 2, 1]
```

**Option 2:** Sort then reverse
```python
nums.sort()
nums.reverse()  # [3, 2, 1]
```

Prefer `reverse=True` — cleaner and single operation.

---

### Custom Sort with key Parameter
**Front:**
How does the `key` parameter work in Python's `sort()`/`sorted()`? 

**Back:**
The `key` parameter accepts a function that transforms each element for comparison (original values are preserved).

```python
# Using a built-in function
words = ["banana", "kiwi", "apple"]
words.sort(key=len)  # ['kiwi', 'apple', 'banana']

# Using a lambda for custom logic
pairs = [(1, 5), (3, 2), (2, 8)]
pairs.sort(key=lambda x: x[1])  # [(3, 2), (1, 5), (2, 8)]

# Other common keys
nums = [-5, 2, -3]
sorted(nums, key=abs)           # [2, -3, -5]

fruits = ["Apple", "banana"]
sorted(fruits, key=str.lower)   # ['Apple', 'banana']
```

**Lambda format:** `lambda <param>: <expression>`

---

### Lambda Functions for Sorting
**Front:**
What is a lambda function? Write a lambda to sort tuples by their second element.

**Back:**
A **lambda** is an anonymous single-expression function.

Format: `lambda <params>: <expression>`

```python
pairs = [(1, 5), (3, 2), (2, 8)]
pairs.sort(key=lambda x: x[1])
# Result: [(3, 2), (1, 5), (2, 8)]
```

Equivalent named function:
```python
def get_second(x):
    return x[1]
pairs.sort(key=get_second)
```

Use lambdas for simple, one-off sort keys.

---

### String Sorting (Lexicographical)
**Front:**
How are strings sorted by default in Python? What's the result of sorting `["grape", "Apple", "banana"]`?

**Back:**
Strings sort **lexicographically** (dictionary order) based on Unicode values.

**Uppercase letters come before lowercase!**

```python
fruits = ["grape", "Apple", "banana"]
fruits.sort()
# Result: ['Apple', 'banana', 'grape']
```

For case-insensitive sort:
```python
fruits.sort(key=str.lower)
# Result: ['Apple', 'banana', 'grape']
```

---

### Unpacking
**Front:**
What is unpacking in Python? Show how to unpack a list/tuple, swap variables, and unpack in a loop.

**Back:**
**Unpacking** extracts values from an iterable into individual variables.

```python
# Basic unpacking
point = [3, 5]
x, y = point  # x = 3, y = 5

# Swap variables (no temp needed!)
a, b = b, a

# Loop unpacking
points = [[0, 0], [2, 4], [3, 6]]
for x, y in points:
    print(f"x: {x}, y: {y}")
```

Must have matching number of variables:
```python
x, y = [1, 2, 3]  # ValueError: too many values to unpack
```

---

### Enumerate
**Front:**
What does `enumerate()` do? Why use it instead of `range(len(list))`?

**Back:**
`enumerate()` returns an iterator of `(index, element)` tuples.

```python
names = ['Alice', 'Bob', 'Charlie']

# Pythonic way
for i, name in enumerate(names):
    print(i, name)

# Instead of
for i in range(len(names)):
    print(i, names[i])
```

More readable and less error-prone than manual indexing.

Optional start index:
```python
for i, name in enumerate(names, start=1):
    print(i, name)  # 1 Alice, 2 Bob, 3 Charlie
```

---

### Zip
**Front:**
What does `zip()` do? What is its time and space complexity?

**Back:**
`zip()` iterates over multiple iterables in parallel, yielding tuples.

```python
names = ['Alice', 'Bob', 'Charlie']
scores = [90, 85, 88]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 90
# Bob: 85
# Charlie: 88
```

**Complexity:** O(1) time and space — returns an iterator, doesn't create a list in memory.

Stops at shortest iterable:
```python
list(zip([1, 2, 3], ['a', 'b']))  # [(1, 'a'), (2, 'b')]
```

---

### List pop() vs pop(index) Time Complexity
**Front:**
What's the time complexity difference between `list.pop()` and `list.pop(index)`? Why?

**Back:**
- `pop()` — O(1): Removes from the end, no shifting needed
- `pop(index)` — O(n): Must shift all elements after the removed index

```python
nums = [1, 2, 3, 4, 5]
nums.pop()      # O(1) - removes 5
nums.pop(0)     # O(n) - removes 1, shifts [2,3,4] left
```

**Implication:** When you need a LIFO structure (stack), use `append()`/`pop()`. Avoid `pop(0)` for queues — use `collections.deque` instead.

---

### List extend() vs Concatenation
**Front:**
What's the difference between `list.extend(other)` and `list + other`?

**Back:**
`extend()`: Modifies the list **in-place**, returns `None`
- Time: O(m) where m = len(other)
- Space: O(1) — no new list created

`+` concatenation: Creates a **new list**
- Time: O(n + m)
- Space: O(n + m) — allocates new list

```python
a = [1, 2]
b = [3, 4]

a.extend(b)    # a is now [1, 2, 3, 4], returns None
c = a + b      # c is new list, a unchanged
```

**Use `extend()`** when building up a list. **Use `+`** when you need the original unchanged.

---

### List Shallow Copy vs Deep Copy
**Front:**
When do you need `copy.deepcopy()` instead of `list.copy()` for lists?

**Back:**
**Shallow copy** (`list.copy()`, `list[:]`, `list(original)`): Copies the list structure but **shares references** to nested objects.

**Deep copy** (`copy.deepcopy()`): Recursively copies all nested objects.

```python
import copy

original = [[1, 2], [3, 4]]

shallow = original.copy()
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] — original changed!

deep = copy.deepcopy(original)
deep[0][0] = 0
print(original)  # [[99, 2], [3, 4]] — original unchanged
```

**Rule:** Use `deepcopy()` when your list contains mutable objects (lists, dicts, sets, custom objects).

---

### List Membership Check is O(n)
**Front:**
What's the time complexity of `x in my_list`? What's the implication?

**Back:**
**O(n)** — Python must scan the list sequentially until it finds the element or reaches the end.

```python
my_list = [1, 2, 3, ..., 1000000]
999999 in my_list  # Checks up to 999,999 elements
```

**Implication:** If you need frequent membership checks, convert to a set:

```python
my_set = set(my_list)  # O(n) one-time cost
999999 in my_set       # O(1) per lookup
```

Lists are for ordered sequences. Sets are for fast membership testing.

---

### List insert() is O(n)
**Front:**
What is the time complexity of `list.insert(index, value)`? Why?

**Back:**
**O(n)**. Inserting at position `i` requires **shifting all elements from index `i` onward** one position to the right.

```python
nums = [1, 2, 3, 4, 5]
nums.insert(0, 0)  # Worst case: shifts ALL elements
# [0, 1, 2, 3, 4, 5]
```

- Insert at beginning: O(n) — shift everything
- Insert at end: O(1) — same as append
- Insert at middle: O(n) — shift half

**Prefer `append()`** when possible. If you need efficient insertion at both ends, use `collections.deque`.

---

### List Comprehension Limitations
**Front:**
What control flow statements can you NOT use inside a list comprehension?

**Back:**
You cannot use `break` or `continue` inside list comprehensions.

```python
# This won't work:
[x for x in range(10) if x == 5 break]  # SyntaxError

# Use a regular loop instead:
result = []
for x in range(10):
    if x == 5:
        break
    result.append(x)
```

List comprehensions are for **transformations and filtering**, not complex control flow. If you need `break`/`continue`, use a regular loop.

---

### List remove() — By Value, Not Index
**Front:**
How does `list.remove(value)` differ from `list.pop(index)`?

**Back:**
`remove(value)`: Deletes the **first occurrence** of a value
- Raises `ValueError` if not found
- O(n) — must search then shift

`pop(index)`: Deletes by **position** and returns the removed element
- Raises `IndexError` if out of bounds
- O(n) for arbitrary index, O(1) for last element

```python
nums = [1, 2, 3, 2, 4]

nums.remove(2)     # [1, 3, 2, 4] — removes first 2
nums.pop(1)        # [1, 2, 4] — removes element at index 1
```

**Use `remove()`** when you know the value. **Use `pop()`** when you know the position.

---

### List index() vs in Operator
**Front:**
When should you use `list.index(value)` vs `value in list`?

**Back:**
`value in list`: Returns `True`/`False` — use when you only need **existence**

`list.index(value)`: Returns the **position** — use when you need to know **where**

```python
names = ['Alice', 'Bob', 'Charlie']

# Just checking existence
if 'Bob' in names:
    print("Found!")

# Need the position
pos = names.index('Bob')  # 1
names[pos] = 'Robert'
```

**Caution:** `index()` raises `ValueError` if not found. Check with `in` first if unsure:

```python
if value in my_list:
    pos = my_list.index(value)
```

---

### Using a List as a Stack in Python
**Front:**
How do you use a list as a stack in Python? What operations do you use and what are their time complexities?

**Back:**
Python has no built-in stack—use a list with **LIFO** (Last In, First Out) semantics.

```python
stack = []
stack.append(1)      # Push
stack.append(2)
top = stack[-1]      # Peek (2)
removed = stack.pop() # Pop (2)
```

**Time Complexity:**
- `append(x)`: O(1)
- `pop()`: O(1)
- `[-1]` (peek): O(1)
- `len()`: O(1)

---

### Python Queue with collections.deque
**Front:**
How do you implement a queue in Python? Show the import, basic operations, and explain the ordering.

**Back:**
Use `collections.deque` for **FIFO** (First In, First Out) queues.

```python
from collections import deque

queue = deque()
queue.append(1)      # Enqueue: [1]
queue.append(2)      # Enqueue: [1, 2]
first = queue.popleft()  # Dequeue: returns 1, queue is [2]
```

- `append()` adds to the right (back of queue)
- `popleft()` removes from the left (front of queue)

Both operations are O(1).

---

### Why deque Over List for Queues
**Front:**
Why should you use `collections.deque` instead of a list for queue operations in Python?

**Back:**
**Lists are dynamic arrays**, **deques are doubly linked lists**.

Removing from the front:
- `list.pop(0)`: **O(n)** — must shift all remaining elements left
- `deque.popleft()`: **O(1)** — just update pointers

```python
# Bad - O(n) per operation
queue = []
queue.append(1)
queue.pop(0)  # Shifts everything

# Good - O(1) per operation
from collections import deque
queue = deque()
queue.append(1)
queue.popleft()  # No shifting
```

**Note:** For multi-threaded code, use `queue.Queue` which provides thread-safe operations.

---

### deque Operations and Time Complexity
**Front:**
What are the four `deque` operations for adding/removing from both ends, and their time complexities? What about indexing?

**Back:**
`deque` is a **double-ended queue**—efficient operations at both ends.

**Operations (all O(1)):**
- `append(x)` — add to right
- `appendleft(x)` — add to left
- `pop()` — remove from right
- `popleft()` — remove from left

**Indexing:**
- `[0]`, `[-1]` (first/last): **O(1)**
- `[i]` (arbitrary index): **O(n)**

```python
from collections import deque
d = deque([1, 2, 3])
d.appendleft(0)  # [0, 1, 2, 3]
d.pop()          # [0, 1, 2], returns 3
```

---

### Working with 2D Lists: Indexing and Dimensions
**Front:**
How do you access elements and get dimensions of a 2D list in Python? How do you get the number of rows and columns?

**Back:**
**Accessing elements:** Use double indexing `grid[row][col]`

**Getting dimensions:**
- Rows: `len(grid)`
- Columns: `len(grid[0])` (assumes non-empty grid with uniform row lengths)

```python
grid = [
    [1, 2, 3],
    [4, 5, 6]
]

grid[0][2]       # 3 (row 0, column 2)
grid[1][0]       # 4 (row 1, column 0)

rows = len(grid)     # 2
cols = len(grid[0])  # 3
```

---

### The [[value] * n] * m Trap
**Front:**
Why does `[[0] * 3] * 2` cause unexpected behavior when modifying elements?

**Back:**
The `* 2` **replicates the reference** to the same inner list, not independent copies. Both rows point to the same list object in memory.

```python
grid = [[0] * 3] * 2
print(grid)       # [[0, 0, 0], [0, 0, 0]]

grid[0][0] = 1
print(grid)       # [[1, 0, 0], [1, 0, 0]] — both rows changed!
```

**Why:** `[0] * 3` creates one list. `* 2` creates a list containing two references to that same list.

This is one of the most common 2D list bugs in Python.

---

### Proper 2D Grid Initialization
**Front:**
How do you correctly initialize a 2D grid with a default value in Python?

**Back:**
Use **list comprehension** to create independent row lists:

```python
rows, cols = 2, 3

# Correct — each row is a new list
grid = [[0] * cols for _ in range(rows)]
grid[0][0] = 1
print(grid)  # [[1, 0, 0], [0, 0, 0]] — only first row changed

# Also correct (more explicit)
grid = [[0 for _ in range(cols)] for _ in range(rows)]
```

The outer comprehension runs `range(rows)` times, creating a **new** inner list each iteration.

**Time Complexity:** O(n × m) to initialize an n × m grid.

---

### Dict Deletion: del vs pop()
**Front:**
What's the difference between `del d[key]` and `d.pop(key)` for removing dictionary entries?

**Back:**
Both remove key-value pairs, but differ in return value and error handling:

**`del d[key]`**
- Removes the entry, returns nothing
- Raises `KeyError` if key doesn't exist

**`d.pop(key)`**
- Removes and **returns the value**
- Raises `KeyError` if key doesn't exist
- Can provide default: `d.pop(key, default)` — returns default instead of error

```python
d = {'a': 1, 'b': 2}

del d['a']              # d is now {'b': 2}
del d['x']              # KeyError: 'x'

value = d.pop('b')      # value = 2, d is now {}
d.pop('x')              # KeyError: 'x'
d.pop('x', 'missing')   # Returns 'missing', no error
```

**Tip:** For safe access without deletion, use `.get(key, default)`.

---

### defaultdict for Cleaner Code
**Front:**
What is `defaultdict` and when should you use it?

**Back:**
`defaultdict` is a dict subclass that automatically creates missing keys with a default value. Avoids `KeyError` on first access.

```python
from collections import defaultdict

# With int — default is 0 (great for counting)
freq = defaultdict(int)
freq['a'] += 1          # No KeyError, 'a' starts at 0

# With list — default is [] (great for grouping)
groups = defaultdict(list)
groups['team'].append('Alice')  # No need to check if key exists

# With lambda — custom default value
scores = defaultdict(lambda: 100)
print(scores['new_player'])  # 100
```

**Common patterns:**
- `defaultdict(int)` — counting/frequency
- `defaultdict(list)` — grouping items
- `defaultdict(set)` — unique grouping
- `defaultdict(lambda: value)` — custom default

---

### Counter for Frequency Counting
**Front:**
What is `Counter` and how do you use it to count occurrences?

**Back:**
`Counter` is a dict subclass optimized for counting. Pass any iterable to count its elements.

```python
from collections import Counter

nums = [1, 2, 2, 3, 3, 3]
freq = Counter(nums)
print(freq)  # Counter({3: 3, 2: 2, 1: 1})

# Access counts (returns 0 for missing keys, no KeyError)
freq[3]     # 3
freq[100]   # 0

# Increment counts
freq[1] += 1  # freq[1] is now 2

# Merge counts with update()
more = [3, 4, 4]
freq.update(more)
print(freq)  # Counter({3: 4, 2: 2, 1: 2, 4: 2})
```

**When to use:**
- `Counter` — simplest for counting (pass iterable directly)
- `defaultdict(int)` — when you need more dict-like behavior
- `dict.get()` — when you can't import collections or want to stick to default classes

---

### Dict and Set Comprehension
**Front:**
What is the syntax for dict and set comprehension in Python?

**Back:**
Similar to list comprehension, but with different brackets:

**Dict comprehension** — use `{key: value for ...}`
```python
nums = [1, 2, 3]
squared = {n: n * n for n in nums}
# {1: 1, 2: 4, 3: 9}

# With condition
even_squared = {n: n * n for n in nums if n % 2 == 0}
# {2: 4}
```

**Set comprehension** — use `{value for ...}` (no colon)
```python
nums = [1, 2, 2, 3, 3, 3]
unique_doubled = {n * 2 for n in nums}
# {2, 4, 6}
```

**Comparison:**
- List: `[expr for ...]`
- Set: `{expr for ...}`
- Dict: `{key: value for ...}`
- Note: no tuple comprehension - must be explicit: `tuple(x for x in range(5))`

---

### Iterating Over Dicts: keys(), values(), items()
**Front:**
What do `keys()`, `values()`, and `items()` return, and what are their time complexities?

**Back:**
They return **view objects** — live views into the dict, not copies. Views update automatically when the dict changes.

```python
d = {'a': 1, 'b': 2, 'c': 3}

d.keys()    # dict_keys(['a', 'b', 'c'])
d.values()  # dict_values([1, 2, 3])
d.items()   # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Views are live — they reflect changes to the dict
keys = d.keys()
print(keys)     # dict_keys(['a', 'b', 'c'])
d['d'] = 4
print(keys)     # dict_keys(['a', 'b', 'c', 'd']) — updated!
```

**Time Complexity:**
- Creating the view: **O(1)** (it's just a reference)
- Iterating through: **O(n)**

**Common pattern** — use `items()` to loop over key-value pairs:
```python
for key, value in d.items():
    print(f"{key}: {value}")
```

Convert to list if needed: `list(d.keys())`

---

### Set Operations: add(), remove(), discard()
**Front:**
How do you add and remove elements from a set? What's the difference between the two removal methods?

**Back:**
**Adding elements:**
```python
s = set()
s.add('a')      # {'a'}
s.add('b')      # {'a', 'b'}
```

**Removing elements:**
```python
s = {'a', 'b', 'c'}

s.remove('a')   # {'b', 'c'} — raises KeyError if not found
s.discard('b')  # {'c'} — NO error if not found
s.discard('x')  # {'c'} — silent, no error
s.remove('x')   # KeyError: 'x'
```

**Key difference:**
- `remove()` — raises `KeyError` if element missing
- `discard()` — silently does nothing if element missing

**Note:** `pop()` exists but removes an arbitrary element (not random, just unspecified order). Use when you need any element from the set.

**Note:** Dicts don't have `.add()` — use `d[key] = value` for insertion.

---

### Tuple Keys in Dicts and Sets
**Front:**
Why can tuples be used as dict keys or set members, but lists cannot?

**Back:**
Dict keys and set members must be **hashable** (immutable). Tuples are immutable; lists are not.

```python
# Tuples work as keys
grid = {}
grid[(0, 0)] = 'start'
grid[(1, 2)] = 'end'

# Tuples work in sets
visited = set()
visited.add((0, 0))
visited.add((1, 2))
(0, 0) in visited  # True

# Lists do NOT work
grid[[0, 0]] = 'x'  # TypeError: unhashable type: 'list'
visited.add([0, 0]) # TypeError: unhashable type: 'list'
```

**Common pattern:** Use `(row, col)` tuples to track grid positions in BFS/DFS.

**Why?** If a list could be a key and you modified it after insertion, the hash would change and the dict/set couldn't find it anymore.

---

