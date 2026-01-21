# Python Data Analysis Anki Cards

## Sources
- [Python for Data Analysis](https://wesmckinney.com/book/)

## Cards

### Strings Are Immutable
**Front:**
Why does this code raise an error? How could you do it instead (2 ways)?
```python
s = "hello"
s[0] = "H"
```

**Back:**
Strings are **immutable** in Python — you cannot modify individual characters in place.

```python
s = "hello"
s[0] = "H"  # TypeError: 'str' object does not support item assignment
```

**Fix:** Use `replace()` or slicing to create a new string:
```python
s = "hello"
s = s.replace("h", "H")  # "Hello" (replaces first occurrence)

# Or with slicing
s = "H" + s[1:]  # "Hello"
```

`replace()` returns a new string — the original is unchanged unless you reassign.

---

### isinstance for Type Checking
**Front:**
How do you check if a variable is an instance of one or more types in Python? Why is this preferred over `type(x) == SomeType`?

**Back:**
Use `isinstance(obj, type)` or `isinstance(obj, (type1, type2, ...))` for multiple types:

```python
a = 5
isinstance(a, int)           # True
isinstance(a, (int, float))  # True — matches either type

b = 4.5
isinstance(b, (int, float))  # True
```

**Why prefer `isinstance()` over `type()`:**
- Handles inheritance — `isinstance(obj, Parent)` returns `True` for subclasses
- `type(x) == int` fails for subclasses of int
- More Pythonic and flexible

```python
class MyInt(int):
    pass

x = MyInt(5)
type(x) == int      # False
isinstance(x, int)  # True
```

---

### f-string Format Specifiers
**Front:**
How do you use f-string format specifiers for:
- Limiting decimal places (e.g., 2 decimals)?
- Zero-padding integers (e.g., 5 digits)?
- Adding thousands separators?
- Right/left aligning with padding?
- Formatting as a percentage?

**Back:**
Format syntax: `{value:specifier}`

**Floats:**
```python
pi = 3.14159
f"{pi:.2f}"    # '3.14' — 2 decimal places
f"{pi:.0f}"    # '3' — no decimals (rounds)
f"{pi:8.2f}"   # '    3.14' — 8 chars wide, 2 decimals
```

**Integers:**
```python
n = 42
f"{n:d}"       # '42' — decimal integer
f"{n:05d}"     # '00042' — zero-padded, 5 chars wide
f"{n:,}"       # '1,000,000' — with thousands separator (for n=1000000)
```

**Strings:**
```python
s = "hi"
f"{s:s}"       # 'hi' — string (usually omitted)
f"{s:>10}"     # '        hi' — right-align, 10 chars wide
f"{s:<10}"     # 'hi        ' — left-align
```

**Percentages:**
```python
rate = 0.856
f"{rate:.1%}"  # '85.6%' — as percentage with 1 decimal
```

---

### datetime: Parsing and Formatting
**Front:**
How do you convert between `datetime` objects and strings in Python? What methods do you use?

**Back:**
**datetime → string:** Use `strftime()` (string format time)
```python
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30)
dt.strftime("%Y-%m-%d")        # '2024-03-15'
dt.strftime("%Y-%m-%d %H:%M")  # '2024-03-15 14:30'
```

**string → datetime:** Use `strptime()` (string parse time)
```python
datetime.strptime("20240315", "%Y%m%d")
# datetime(2024, 3, 15, 0, 0)

datetime.strptime("2024-03-15 14:30", "%Y-%m-%d %H:%M")
# datetime(2024, 3, 15, 14, 30)
```

**Common format codes:**
- `%Y` — 4-digit year (2024)
- `%m` — 2-digit month (03)
- `%d` — 2-digit day (15)
- `%H` — 24-hour hour (14)
- `%M` — minute (30)
- `%S` — second

**Mnemonic:** `strftime` = "format", `strptime` = "parse"

---

### timedelta Arithmetic
**Front:**
How do you perform date/time arithmetic in Python? What type results from subtracting two `datetime` objects?

**Back:**
Subtracting two `datetime` objects returns a `timedelta`:

```python
from datetime import datetime, timedelta

dt1 = datetime(2024, 3, 15, 10, 0)
dt2 = datetime(2024, 3, 10, 8, 0)

delta = dt1 - dt2
print(delta)        # 5 days, 2:00:00
print(type(delta))  # <class 'datetime.timedelta'>
```

**Add/subtract timedelta from datetime:**
```python
dt = datetime(2024, 3, 15)

dt + timedelta(days=7)          # 2024-03-22
dt - timedelta(hours=3)         # 2024-03-14 21:00:00
dt + timedelta(days=1, hours=2) # 2024-03-16 02:00:00
```

**Access timedelta components:**
```python
delta = timedelta(days=5, hours=3, minutes=30)
delta.days           # 5
delta.seconds        # 12600 (3*3600 + 30*60)
delta.total_seconds() # 450600.0 (entire duration in seconds)
```

---

### Mutating Mutable Objects Inside Tuples
**Front:**
Tuples are immutable, so why does this code work without error?
```python
tup = ([1, 2], [3, 4])
tup[0].append(5)
print(tup)
```

**Back:**
Tuples are immutable **containers** — you can't reassign their elements. But if an element is mutable (like a list), you can still mutate that object.

```python
tup = ([1, 2], [3, 4])
tup[0].append(5)
print(tup)  # ([1, 2, 5], [3, 4])

tup[0] = [9, 9]  # TypeError: 'tuple' object does not support item assignment
```

The tuple holds *references* to objects. You can't change which objects it references, but you can change the objects themselves if they're mutable.

**Practical implication:** A tuple containing mutable elements cannot be used as a dict key or in a set — it's unhashable.

---

### Extended Unpacking with *rest
**Front:**
How do you unpack the first two elements of an iterable and capture the rest? What convention indicates you don't need the remaining values?

**Back:**
Use `*rest` to capture remaining elements as a list:

```python
values = [1, 2, 3, 4, 5]

a, b, *rest = values
# a = 1, b = 2, rest = [3, 4, 5]

first, *middle, last = values
# first = 1, middle = [2, 3, 4], last = 5
```

**Convention:** Use `*_` when you don't need the remaining values:

```python
a, b, *_ = values  # Discard everything after first two
```

The `*` variable is always a list, even if it captures zero or one element:

```python
a, b, *rest = [1, 2]
# rest = []
```

---

### dict.setdefault() Method
**Front:**
What does `dict.setdefault(key, default)` do? When would you use it instead of `defaultdict`?

**Back:**
`setdefault` returns the value if the key exists; otherwise it **inserts** the default and returns it.

```python
by_letter = {}
for word in ["apple", "bat", "bar", "atom"]:
    letter = word[0]
    by_letter.setdefault(letter, []).append(word)

# {'a': ['apple', 'atom'], 'b': ['bat', 'bar']}
```

**`setdefault` vs `defaultdict`:**
- `setdefault` — use when you need default behavior for just one key or a few operations, without changing the dict type
- `defaultdict` — use when building up a dict and you want automatic defaults throughout

```python
# setdefault: selective use
regular_dict = {"a": 1}
regular_dict.setdefault("b", 0)  # Only for this access

# defaultdict: consistent behavior
from collections import defaultdict
auto_dict = defaultdict(int)  # All missing keys default to 0
```

`setdefault` keeps your dict a regular `dict`; `defaultdict` changes the type.

---

### Creating a Dict from Two Sequences
**Front:**
How do you create a dictionary from two parallel sequences (one for keys, one for values)?

**Back:**
Use `dict()` with `zip()`:

```python
keys = ['a', 'b', 'c']
values = [1, 2, 3]

d = dict(zip(keys, values))
# {'a': 1, 'b': 2, 'c': 3}
```

If sequences have different lengths, `zip` stops at the shortest:

```python
keys = ['a', 'b', 'c', 'd']
values = [1, 2]
dict(zip(keys, values))  # {'a': 1, 'b': 2}
```

**Alternative:** Dict comprehension for more control:

```python
d = {k: v for k, v in zip(keys, values)}

# With transformation
d = {k: v * 2 for k, v in zip(keys, values)}
```

---

### Set Operations: Union, Intersection, Difference
**Front:**
How do you compute the union, intersection, difference, and symmetric difference of two sets in Python?

**Back:**
Each operation has both a method and an operator:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
```

- **Union** — elements in either set:
  - `a | b` or `a.union(b)` → `{1, 2, 3, 4, 5, 6}`

- **Intersection** — elements in both sets:
  - `a & b` or `a.intersection(b)` → `{3, 4}`

- **Difference** — elements in `a` but not in `b`:
  - `a - b` or `a.difference(b)` → `{1, 2}`

- **Symmetric difference** — elements in either but not both:
  - `a ^ b` or `a.symmetric_difference(b)` → `{1, 2, 5, 6}`

**In-place versions** modify `a` directly (each example starts fresh):
```python
a = {1, 2, 3, 4}; a |= b   # a is now {1, 2, 3, 4, 5, 6}
a = {1, 2, 3, 4}; a &= b   # a is now {3, 4}
a = {1, 2, 3, 4}; a -= b   # a is now {1, 2}
a = {1, 2, 3, 4}; a ^= b   # a is now {1, 2, 5, 6}
```

---

### Set Subset and Superset Checks
**Front:**
How do you check if one set is a subset or superset of another in Python?

**Back:**
Use `issubset()` / `issuperset()` methods or comparison operators:

```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

a.issubset(b)     # True — all elements of a are in b
a <= b            # True — same as issubset

b.issuperset(a)   # True — b contains all elements of a
b >= a            # True — same as issuperset
```

**Strict subset/superset** (not equal):
```python
a < b   # True — a is a proper subset (subset but not equal)
b > a   # True — b is a proper superset

{1, 2} < {1, 2}   # False — not a proper subset
{1, 2} <= {1, 2}  # True — is a subset (or equal)
```

**Common use:** Checking if required fields are present:
```python
required = {'name', 'email'}
provided = {'name', 'email', 'phone'}
required <= provided  # True — all required fields present
```

---

### Iterators and Generators
**Front:**
What is an iterator in Python? What is a generator, and why are generators useful?

**Back:**
An **iterator** is any object that yields values one at a time when used in a `for` loop or with `next()`. Most built-in functions accepting "list-like" objects also accept iterators (`min`, `max`, `sum`, `list`, `tuple`).

A **generator** is a function that produces an iterator using `yield` instead of `return`:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(3):
    print(num)  # 3, 2, 1
```

**Why generators matter:**
- **Memory efficiency** — values are produced one at a time, not stored in memory all at once
- **Lazy evaluation** — computation happens only when values are requested
- **Infinite sequences** — can represent unbounded data streams

**Critical for ML/data work:** When processing millions of rows, a generator avoids loading everything into memory.

```python
# Bad: loads entire file into memory
lines = open('huge.csv').readlines()

# Good: processes line by line
for line in open('huge.csv'):
    process(line)
```

---

### yield vs return
**Front:**
What's the difference between `yield` and `return` in a Python function?

**Back:**
`return` exits the function and sends back a value. The function's state is lost.

`yield` **pauses** the function and sends back a value. The function's state is preserved, and execution resumes from that point on the next call.

```python
def with_return():
    return 1

def with_yield():
    yield 1
    yield 2
    yield 3

with_return()        # Returns: 1 (an integer)
with_yield()         # Returns: <generator object> (not 1!)

list(with_return())  # list(1) → Error: int is not iterable
list(with_yield())   # [1, 2, 3] — list() iterates the generator to exhaustion
```

**Key insight:** Calling a generator function doesn't execute its body — it returns a generator object. That object is iterable, and `list()` iterates it until `StopIteration`, collecting each yielded value.

**Execution flow:**
```python
def gen():
    print("Start")
    yield 1
    print("After first yield")
    yield 2
    print("End")

g = gen()          # Nothing printed yet
next(g)            # Prints "Start", returns 1
next(g)            # Prints "After first yield", returns 2
next(g)            # Prints "End", raises StopIteration
```

A function with `yield` becomes a **generator function** — calling it returns a generator object, it doesn't execute the function body immediately.

---

### Functions as First-Class Objects
**Front:**
What does it mean that functions are "first-class objects" in Python? Show an example of storing functions in a data structure.

**Back:**
Functions can be assigned to variables, stored in data structures, and passed as arguments — just like any other object.

```python
import re

def remove_punctuation(value):
    return re.sub("[!#?]", "", value)

# Store functions in a list
clean_ops = [str.strip, remove_punctuation, str.title]

def clean_strings(strings, ops):
    result = []
    for value in strings:
        for func in ops:
            value = func(value)
        result.append(value)
    return result

states = ["  Alabama ", "Georgia!", "florida"]
clean_strings(states, clean_ops)
# ['Alabama', 'Georgia', 'Florida']
```

**Key insight:** `str.strip` and `str.title` are unbound methods — when called with a string argument, Python treats it as the `self` parameter.

**Using `map()`** — applies one function to each element, so chain calls for multiple operations:
```python
# Step by step
result = map(str.strip, states)
result = map(remove_punctuation, result)
result = list(map(str.title, result))
# ['Alabama', 'Georgia', 'Florida']

# Or nested (reads inside-out)
list(map(str.title, map(remove_punctuation, map(str.strip, states))))
```

**Common patterns:**
- Passing functions to `map()`, `filter()`, `sorted(key=...)`
- Storing callbacks or handlers in a dict
- Building pipelines of transformations

---

### else Block with try/except
**Front:**
What does the `else` block do in a `try/except` statement? When does it run?

**Back:**
The `else` block runs **only if no exception was raised** in the `try` block:

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        print("Division successful")
        return result

safe_divide(10, 2)   # Prints "Division successful", returns 5.0
safe_divide(10, 0)   # Prints "Cannot divide by zero", returns None
```

**Why use `else` instead of putting code in `try`?**
- Keeps the `try` block minimal — only code that might raise the exception
- Makes intent clear — "do this if everything succeeded"
- Avoids accidentally catching exceptions from code that shouldn't be protected

```python
try:
    value = int(user_input)
except ValueError:
    print("Invalid number")
else:
    # Only runs if conversion succeeded
    # Exceptions here are NOT caught by the except above
    process(value)
```

**Full structure:** `try` → `except` → `else` → `finally`

---

