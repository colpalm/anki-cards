# Python Fundamentals Anki Cards

## Card 1: Floor Division with Negatives
**Front:**
What is the result of `-7 // 2` in Python? Why?

**Back:**
`-4`

Floor division rounds *down* (toward negative infinity), not toward zero.
- `-7 / 2 = -3.5`
- Rounding down gives `-4`

Contrast with integer division in C/Java which truncates toward zero (would give `-3`).

---

## Card 2: Boolean Operator Precedence
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

## Card 3: Falsy Values
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

## Card 4: Mutable Default Argument Pitfall
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

## Card 5: String Reversal with Slicing
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

## Card 6: Negative Indexing
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

## Card 7: Dictionary .get() Method
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

## Card 8: Empty Set Creation
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

## Card 9: Generator Expression vs List Comprehension
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

## Card 10: Different Error Types
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

## Card 11: .sort() vs sorted()
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

## Card 12: Reverse Sorting
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

## Card 13: Custom Sort with key Parameter
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

## Card 14: Lambda Functions for Sorting
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

## Card 15: String Sorting (Lexicographical)
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

