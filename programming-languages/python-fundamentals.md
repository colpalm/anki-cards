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

