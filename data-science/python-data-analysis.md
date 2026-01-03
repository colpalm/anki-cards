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

