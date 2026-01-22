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

---

### What is a class method?

**Front:**
What is a class method in Python, and when would you use one?

**Back:**
A **class method** operates on the class itself rather than on instances. It receives the class as its first argument (`cls`) instead of an instance (`self`).

**Common use cases:**
- Factory methods / alternative constructors
- Tracking class-level state (e.g., counting instances)
- Methods that need to work with the class, not a specific instance

```python
class SuperHero:
    hero_count = 0

    def __init__(self, name):
        self.name = name
        SuperHero.hero_count += 1

    @classmethod
    def from_alias(cls, alias, real_name):
        """Factory method - alternative constructor"""
        return cls(f"{alias} ({real_name})")

hero = SuperHero.from_alias("Spider-Man", "Peter Parker")
print(hero.name)  # Spider-Man (Peter Parker)
```

---

### How to define a class method

**Front:**
How do you define and call a class method in Python?

**Back:**
Use the `@classmethod` decorator and accept `cls` as the first parameter.

```python
class SuperHero:
    base_power = 100

    @classmethod
    def get_base_power(cls):
        return cls.base_power

    @classmethod
    def set_base_power(cls, power):
        cls.base_power = power

# Call via the class (preferred)
print(SuperHero.get_base_power())  # 100

# Also works via an instance
hero = SuperHero()
print(hero.get_base_power())  # 100
```

`cls` is a convention (like `self`), not a keyword—but always use `cls` to be idiomatic.

---

### Why use `cls` instead of the class name?

**Front:**
In a class method, why should you use `cls` instead of the class name directly?

**Back:**
Using `cls` respects inheritance—it refers to the actual calling class, which may be a subclass. Hardcoding the class name breaks polymorphism.

```python
class Animal:
    count = 0

    @classmethod
    def create(cls):
        cls.count += 1
        return cls()

class Dog(Animal):
    pass

dog = Dog.create()  # cls is Dog, not Animal
print(Dog.count)     # 1
print(Animal.count)  # 0 (separate counter)
```

If we used `Animal.count` instead of `cls.count`, all subclasses would share the same counter—which is rarely what you want.

**Rule of thumb:** Always use `cls` in class methods unless you explicitly need to reference a specific class.

---

### What is a static method?

**Front:**
What is a static method in Python, and when would you use one?

**Back:**
A **static method** belongs to a class but doesn't access the class (`cls`) or instance (`self`). It's essentially a regular function namespaced to the class.

**Use cases:**
- Utility functions logically related to the class
- Helper methods that don't need class or instance state
- Grouping related functionality under a class namespace

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))

print(MathUtils.is_even(4))       # True
print(MathUtils.clamp(15, 0, 10)) # 10
```

If the method doesn't use `self` or `cls`, it's a candidate for `@staticmethod`.

---

### How to define a static method

**Front:**
How do you define a static method in Python?

**Back:**
Use the `@staticmethod` decorator. The method takes no implicit first argument—no `self` or `cls`.

```python
class SuperHero:
    @staticmethod
    def validate_name(name):
        return len(name) > 0 and name[0].isupper()

# Call via the class
print(SuperHero.validate_name("Spider-Man"))  # True

# Also works via an instance
hero = SuperHero()
print(hero.validate_name("spider-man"))  # False
```

**Note:** A static method can still access class attributes, class methods or static methods, but only via the class name directly (`ClassName.attr`).

---

### Class method vs static method

**Front:**
When should you use a class method vs a static method?

**Back:**
**Use `@classmethod` when you need:**
- Access to the class (`cls`) or class attributes
- Factory methods / alternative constructors
- Inheritance-aware behavior (subclasses get their own `cls`)

**Use `@staticmethod` when you need:**
- A utility function that belongs logically to the class
- No access to class or instance state
- A function that could be standalone but is related to the class

```python
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, date_str):
        """Factory method - needs cls to create instance"""
        y, m, d = map(int, date_str.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid_date(date_str):
        """Pure validation - doesn't need class or instance"""
        parts = date_str.split("-")
        return len(parts) == 3 and all(p.isdigit() for p in parts)

print(Date.is_valid_date("2024-01-15"))  # True
d = Date.from_string("2024-01-15")
```

**Simple rule:** If you need `cls`, use `@classmethod`. If you don't need `cls` or `self`, use `@staticmethod`.

---

### What is inheritance?

**Front:**
What is inheritance in Python? What happens to the parent's `__init__` when you create a child class?

**Back:**
**Inheritance** allows a child class (subclass) to reuse attributes and methods from a parent class (superclass).

```python
class SuperHero:
    def __init__(self, name, power):
        self.name = name
        self.power = power

class Avenger(SuperHero):
    def assemble(self):
        print(f"{self.name} assembles!")

# Avenger inherits __init__, name, and power from SuperHero
iron_man = Avenger("Iron Man", "repulsor beams")
print(iron_man.name)   # Iron Man
iron_man.assemble()    # Iron Man assembles!
```

**Parent `__init__` behavior:**
- If child has no `__init__`, parent's `__init__` is called automatically
- If child defines `__init__`, you must explicitly call `super().__init__()` to run the parent's initialization

---

### Method overriding

**Front:**
What is method overriding in Python? When would you use it?

**Back:**
**Method overriding** is when a child class defines a method with the same name as one in the parent class, replacing the parent's behavior.

```python
class SuperHero:
    def fight(self):
        print("Fighting with basic moves!")

class Avenger(SuperHero):
    def fight(self):  # Overrides parent method
        print("Fighting with advanced weapons!")

hero = Avenger()
hero.fight()  # Fighting with advanced weapons!
```

**When to use:**
- When the parent's implementation doesn't fit the child's needs
- When you want to specialize behavior for the subclass

To extend (rather than replace) the parent's behavior, use `super().method_name()` inside the override.

---

### The super() function

**Front:**
What does `super()` do in Python? How do you use it with `__init__`?

**Back:**
`super()` returns a proxy object that lets you call methods from the parent class. Most commonly used to call the parent's `__init__`.

```python
class SuperHero:
    def __init__(self, name, power):
        self.name = name
        self.power = power

class Avenger(SuperHero):
    def __init__(self, name, power, team):
        super().__init__(name, power)  # Call parent's __init__
        self.team = team               # Add child-specific attribute

avenger = Avenger("Iron Man", "repulsor beams", "Avengers")
print(avenger.name)  # Iron Man (from parent)
print(avenger.team)  # Avengers (from child)
```

**Key points:**
- You must pass the arguments the parent's `__init__` expects
- Also works for calling other parent methods: `super().method_name()`
- Using `super()` (vs hardcoding the parent class name) properly supports multiple inheritance

---

### Multiple inheritance

**Front:**
What is multiple inheritance in Python? Why is it generally discouraged?

**Back:**
**Multiple inheritance** allows a class to inherit from more than one parent class.

```python
class Swimmer:
    def swim(self):
        print("Swimming")

class Flyer:
    def fly(self):
        print("Flying")

class Duck(Swimmer, Flyer):
    pass

duck = Duck()
duck.swim()  # Swimming
duck.fly()   # Flying
```

**Why it's discouraged:**
- Creates complex class hierarchies that are hard to understand
- Can lead to the **diamond problem** (ambiguous method resolution)
- Makes code harder to maintain and debug

**When it might be acceptable:**
- Mixin classes (small, focused classes that add specific behavior)
- When composition isn't a good fit

In most cases, prefer **composition over inheritance**.

---

### Composition vs inheritance (is-a vs has-a)

**Front:**
What's the difference between composition and inheritance? When should you prefer one over the other?

**Back:**
**Inheritance (is-a):** Child class *is a* type of parent. Uses `class Child(Parent)`.

**Composition (has-a):** Class *has* another object as an attribute. Uses instance variables.

```python
# Inheritance: Car IS A Vehicle
class Car(Vehicle):
    pass

# Composition: Car HAS AN Engine
class Car:
    def __init__(self):
        self.engine = Engine()
```

**Prefer composition when:**
- You need flexibility to swap components at runtime
- The relationship is "uses" rather than "is a type of"
- You want to avoid tight coupling to a parent class

**Prefer inheritance when:**
- There's a true "is-a" relationship
- You need to work with existing polymorphic code
- You're extending a framework that expects subclassing

**Rule of thumb:** Default to composition. Use inheritance when there's a clear hierarchical relationship and you need polymorphism.

---

### Diamond problem and MRO

**Front:**
What is the diamond problem in multiple inheritance? How does Python resolve it?

**Back:**
The **diamond problem** occurs when a class inherits from two classes that share a common ancestor, creating ambiguity about which method to call.

```python
class A:
    def greet(self):
        print("A")

class B(A):
    def greet(self):
        print("B")

class C(A):
    def greet(self):
        print("C")

class D(B, C):
    pass

#    A
#   / \
#  B   C
#   \ /
#    D

d = D()
d.greet()  # B — but why?
```

**Method Resolution Order (MRO):** Python uses a deterministic order to find methods:
1. Current class (`D`)
2. First parent (`B`)
3. Second parent (`C`)
4. Common ancestor (`A`)
5. `object`

```python
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

The order of parents in the class definition matters: `class D(B, C)` checks `B` before `C`.

---

### Polymorphism

**Front:**
What is polymorphism? What's the difference between runtime and compile-time polymorphism in Python?

**Back:**
**Polymorphism** means objects of different types can be used through the same interface—the correct behavior is determined by the actual object type.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def animal_sound(animal):
    print(animal.speak())  # Same interface, different behavior

animal_sound(Dog())  # Woof!
animal_sound(Cat())  # Meow!
```

**Runtime polymorphism (dynamic):**
- Determined during execution
- Achieved through method overriding and duck typing
- Most common in Python

**Compile-time polymorphism (static):**
- Determined before code runs
- In other languages: method overloading (same name, different parameters)
- Python doesn't truly support this—uses default args or `*args` instead

---

### Method overloading in Python

**Front:**
Does Python support method overloading? How do you achieve similar behavior?

**Back:**
**Python does not support traditional method overloading.** If you define multiple methods with the same name, only the last one exists—earlier definitions are overwritten.

**Workarounds:**

1. **Default arguments:**
```python
def add(a, b, c=0):
    return a + b + c

add(1, 2)      # 3
add(1, 2, 3)   # 6
```

2. **Variable-length arguments:**
```python
def add(*args):
    return sum(args)

add(1, 2)         # 3
add(1, 2, 3, 4)   # 10
```

3. **Multiple dispatch (third-party):**
```python
from multipledispatch import dispatch

@dispatch(int, int)
def add(x, y):
    return x + y

@dispatch(str, str)
def add(x, y):
    return x + y  # concatenation

add(1, 2)      # 3
add("a", "b")  # "ab"
```

The first two approaches are idiomatic Python; `multipledispatch` is useful for type-based dispatch in larger applications.

---

### Duck typing

**Front:**
What is duck typing in Python? Why is it considered idiomatic?

**Back:**
**Duck typing:** "If it walks like a duck and quacks like a duck, it's a duck." An object's suitability is determined by its methods/attributes, not its class.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Robot:
    def speak(self):
        return "Beep boop!"

def make_speak(thing):
    print(thing.speak())  # Don't care about type, just need speak()

make_speak(Dog())    # Woof!
make_speak(Robot())  # Beep boop!
```

**Why it's idiomatic in Python:**
- Python is dynamically typed—no compile-time type checking
- Enables flexibility without inheritance hierarchies
- Promotes loose coupling (classes don't need to know about each other)

**Trade-off:** No compile-time safety. If an object lacks the required method, you get a runtime `AttributeError`. Use `try/except` or `hasattr()` if needed.

---

### isinstance() and issubclass()

**Front:**
What do `isinstance()` and `issubclass()` do? When would you use them?

**Back:**
**`isinstance(obj, class)`** — checks if an object is an instance of a class (or its subclasses).

**`issubclass(child, parent)`** — checks if a class is a subclass of another.

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()

isinstance(dog, Dog)       # True
isinstance(dog, Animal)    # True (inheritance counts)
isinstance(dog, str)       # False

issubclass(Dog, Animal)    # True
issubclass(Dog, Dog)       # True (class is subclass of itself)
issubclass(Animal, Dog)    # False
```

**When to use:**
- Input validation: `if not isinstance(x, int): raise TypeError(...)`
- When you genuinely need type-specific behavior

**Note:** In idiomatic Python, duck typing and `try/except` are often preferred over explicit type checks. Use these when type actually matters (e.g., API boundaries, serialization).

---

### What is abstraction?

**Front:**
What is abstraction in object-oriented programming?

**Back:**
**Abstraction** is hiding complex implementation details and exposing only the necessary features to the outside world.

```python
class TemperatureConverter:
    def __init__(self, celsius):
        self._celsius = celsius  # Hidden internal state

    def get_fahrenheit(self) -> float:
        return (self._celsius * 9/5) + 32

temp = TemperatureConverter(25)
print(temp.get_fahrenheit())  # 77.0
# User doesn't need to know the conversion formula
```

Think of a TV remote—you press buttons to change channels without understanding the electronics inside.

---

### Abstraction vs encapsulation

**Front:**
What's the difference between abstraction and encapsulation?

**Back:**
**Abstraction** operates at the design level—deciding *what* features to expose and hiding unnecessary complexity.

**Encapsulation** operates at the implementation level—*how* to organize code by bundling data with the methods that operate on it, and restricting direct access.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            return amount
        raise ValueError("Insufficient funds")
```

- **Encapsulation:** `_balance` and `withdraw()` are bundled together; `_balance` is protected from direct access
- **Abstraction:** User calls `withdraw()` without knowing how balance validation works

**Memory aid:** Abstraction = what to show. Encapsulation = how to bundle and protect.

---

### Abstract classes and methods in Python

**Front:**
How do you create an abstract class and abstract method in Python?

**Back:**
Inherit from `ABC` and use the `@abstractmethod` decorator.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, color):
        self.color = color  # Concrete attribute

    @abstractmethod
    def area(self) -> float:
        pass  # No implementation

    def describe(self):  # Concrete method
        return f"A {self.color} shape"

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def area(self) -> float:  # Must implement
        return 3.14159 * self.radius ** 2
```

**Key behaviors:**
- Cannot instantiate abstract classes: `Shape("red")` raises `TypeError`
- Subclasses must implement all abstract methods or they're also abstract
- Abstract classes can have concrete methods and `__init__`

---

### When to use an abstract class

**Front:**
When should you use an abstract class instead of a regular class or interface?

**Back:**
Use an abstract class when you want to **share implementation** while **enforcing a contract**.

**Good fit for abstract class:**
- Common base functionality that subclasses share
- Some methods have sensible defaults, others must be customized
- You want to prevent instantiation of incomplete implementations

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id  # Shared state

    def log_transaction(self, amount):  # Shared implementation
        print(f"Merchant {self.merchant_id}: ${amount}")

    @abstractmethod
    def process(self, amount) -> bool:  # Must be customized
        pass

class StripeProcessor(PaymentProcessor):
    def process(self, amount) -> bool:
        # Stripe-specific implementation
        self.log_transaction(amount)  # Reuse parent method
        return True
```

**Use a regular class** if all methods have implementations.
**Use an interface** if you only need a contract with no shared code.

---

### What is an interface in Python?

**Front:**
What is an interface in Python?

**Back:**
An **interface** is an abstract class that contains *only* abstract methods—a pure contract with no implementation.

```python
from abc import ABC, abstractmethod

class Serializable(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @abstractmethod
    def to_xml(self) -> str:
        pass

class User(Serializable):
    def __init__(self, name):
        self.name = name

    def to_json(self) -> str:
        return f'{{"name": "{self.name}"}}'

    def to_xml(self) -> str:
        return f"<user><name>{self.name}</name></user>"
```

**Key points:**
- Python has no `interface` keyword—uses `ABC` for this purpose
- Interfaces define *what* must be implemented, not *how*
- Avoid adding `__init__` to interfaces (focus on method contracts)

---

### Interface vs abstract class

**Front:**
What's the difference between an interface and an abstract class in Python?

**Back:**
| Aspect | Interface | Abstract Class |
|--------|-----------|----------------|
| Methods | Only abstract | Mix of abstract and concrete |
| Implementation | None | Can share code |
| `__init__` | Avoid | Can have |
| Purpose | Pure contract | Contract + shared behavior |

```python
from abc import ABC, abstractmethod

# Interface: pure contract
class Drawable(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

# Abstract class: contract + shared behavior
class Shape(ABC):
    def __init__(self, color):
        self.color = color

    def describe(self):
        return f"A {self.color} shape"

    @abstractmethod
    def area(self) -> float:
        pass
```

**When to use each:**
- **Interface:** Multiple unrelated classes need the same capability (e.g., `Serializable`, `Comparable`)
- **Abstract class:** Related classes share common behavior and state

