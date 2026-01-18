# Python OOP Anki Cards

## Sources
- [NeetCode Python OOP](https://neetcode.io/problems/python-intro-to-classes/question)

## Cards

### What is a class in Python?

**Front:**
What is a class in Python, and what is an object?

**Back:**
A **class** is a blueprint for creating objects. It defines attributes (data) and methods (behavior).

An **object** is an instance created from that blueprint.

```python
class SuperHero:
    def __init__(self, name, power):
        self.name = name
        self.power = power

# Create an object (instance) of the class
iron_man = SuperHero("Iron Man", "repulsor beams")
```

Class names use PascalCase by convention.

---

### What is the `__init__` method?

**Front:**
What is the `__init__` method in a Python class, and when is it called?

**Back:**
`__init__` is a special method that initializes a new object's attributes. It's automatically called when you create an instance of the class.

```python
class SuperHero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

# __init__ is called automatically here
spider_man = SuperHero("Spider-Man", 100)
```

You don't call `__init__` directly—Python calls it for you when you instantiate the class.

---

### What does `self` represent?

**Front:**
What does `self` represent in Python class methods, and why is it required?

**Back:**
`self` refers to the specific instance the method is acting on. It allows each object to access its own attributes and methods.

```python
class SuperHero:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print(f"I am {self.name}")

hero = SuperHero("Thor")
hero.introduce()  # Python translates this to: SuperHero.introduce(hero)
```

`self` must be the first parameter in instance method definitions, but you don't pass it explicitly—Python handles it automatically.

---

### Instance attributes vs class attributes

**Front:**
What's the difference between instance attributes and class attributes in Python?

**Back:**
**Instance attributes** are defined with `self` and are unique to each object. They are accessed via instance.

**Class attributes** are defined directly in the class body and are shared across all instances. They are accessed via class.

```python
class SuperHero:
    team = "Avengers"  # Class attribute (shared)

    def __init__(self, name):
        self.name = name  # Instance attribute (unique)

hero1 = SuperHero("Iron Man")
hero2 = SuperHero("Thor")

print(hero1.name)        # Iron Man
print(hero2.name)        # Thor
print(SuperHero.team)    # Avengers (accessed via class)
print(hero1.team)        # Avengers (also accessible via instance)
```

**Note:** Class attributes are available from the instance (`hero1.team`)but assigning via instance (e.g., `hero1.team = "X-Men"`) creates a new instance attribute that shadows the class attribute rather than modifying the shared value.

---

### Method vs function

**Front:**
What's the difference between a method and a function in Python?

**Back:**
A **method** is a function defined inside a class. It operates on an instance and receives `self` as its first parameter.

A **function** is defined outside of any class.

```python
# Function (standalone)
def add(a, b):
    return a + b

# Method (belongs to a class)
class Calculator:
    def add(self, a, b):
        return a + b
```

Methods are called on objects using dot notation: `obj.method()`

---

### Accessing and modifying object attributes

**Front:**
What is a simple way to access and modify an object's attributes in Python?

**Back:**
Use **dot notation**: `object.attribute`

```python
class SuperHero:
    def __init__(self, name, health):
        self.name = name
        self.health = health

hero = SuperHero("Iron Man", 100)

# Access
print(hero.name)    # Iron Man
print(hero.health)  # 100

# Modify
hero.health = 80
print(hero.health)  # 80
```

**Note:** For more controlled access, Python supports getter/setter methods and the `@property` decorator.

---

### Docstrings

**Front:**
How do you retrieve a class or method's docstring programmatically in Python?

**Back:**
Use the `__doc__` attribute or the `help()` function.

```python
# Access docstrings
print(SuperHero.__doc__)
print(SuperHero.take_damage.__doc__)
# Full documentation
help(SuperHero)
```

**Docstring best practices:**

- Use triple quotes (`"""`) immediately after the class/method definition
- Follow a consistent style (e.g., Google-style)

For **classes**: describe the purpose and list attributes.

For **methods**: use a one-line description for simple methods. For complex methods, include `Args:`, `Returns:`, and `Raises:` sections.

```python
class SuperHero:
    """
    A class representing a superhero.

    Attributes:
        name (str): The superhero's name.
        health (int): Current health points.
    """

    def take_damage(self, amount: int) -> bool:
        """
        Reduce health by the given amount.

        Args:
            amount (int): Damage to inflict.

        Returns:
            bool: True if hero survived, False otherwise.

        Raises:
            ValueError: If amount is negative.
        """
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        self.health -= amount
        return self.health > 0
```

---

### What is encapsulation?

**Front:**
What is encapsulation in object-oriented programming?

**Back:**
Encapsulation is bundling data and methods that operate on that data within a class, while restricting direct access to some components.

The goal is to hide internal implementation details and expose only what's necessary.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # internal state hidden

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount

    def get_balance(self):
        return self._balance
```

External code interacts through methods rather than directly manipulating internal state—allowing validation, logging, or implementation changes without affecting callers.

Think about a car - don't need to know the internals of the car, just how to use/drive it.

---

### Python's access control conventions

**Front:**
How does Python indicate public, protected, and private attributes? Is access actually enforced?

**Back:**
Python uses naming conventions, not enforcement:

- `name` — Public, accessible everywhere
- `_name` — Protected, signals "internal use"
- `__name` — Private, triggers name mangling

```python
class Example:
    def __init__(self):
        self.public = 1       # no restriction
        self._protected = 2   # convention: don't access externally
        self.__private = 3    # mangled to _Example__private

obj = Example()
obj._protected    # works (but discouraged)
obj._Example__private  # works (mangling is not security)
```

**In practice:** Single underscore `_` is the standard convention. Double underscore `__` is rarely used—it exists mainly to avoid name collisions in inheritance, not for "true" privacy.

---

### The @property decorator

**Front:**
How do you use the `@property` decorator to create a getter and setter in Python?

**Back:**
`@property` creates a getter; `@<name>.setter` creates a setter. Both use the same method name.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.radius)  # calls getter → 5
c.radius = 10    # calls setter
```

This is the Pythonic alternative to Java-style `get_radius()` / `set_radius()` methods—cleaner syntax while still allowing validation.

---

### When to use @property vs public attributes

**Front:**
When should you use `@property` versus a plain public attribute in Python?

**Back:**
**Start with public attributes.** Add `@property` only when you need:

1. **Validation** - enforce constraints on assignment
2. **Computed values** - derive from other attributes
3. **Side effects** - logging, caching, lazy loading
4. **Backward compatibility** - replace an attribute without breaking callers

```python
# Start simple
class User:
    def __init__(self, email):
        self.email = email  # public is fine

# Add @property later if needed
class User:
    def __init__(self, email):
        self._email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value
```

Unlike Java, you don't need getters/setters "just in case"—you can add them later without changing the public interface.

