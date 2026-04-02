# Python Note

## Numeric Types

### int
```python
# whole numbers
x = 10
```

### float
```python
# decimal numbers
y = 3.14
z = 10 / 3  # result is float
```

## Text Data

### String (str)
```python
# text data
text = "data analysis"
```

### f-string 
A placeholder can contain variables, modifiers, or Python code (like math operations).

```python
# Basic f-string
name = "Hy"
age = 25
txt = f"My name is {name}, I am {age}"

# Modifiers (e.g., fixed point number with 2 decimals)
price = 59
txt_price = f"The price is {price:.2f} dollars"

# Math operations inside the placeholder
txt_math = f"The price is {20 * 59} dollars"
```

### String Slicing
By leaving out the start index, the range will start at the first character.

Basic Slice: specify start index and end index (not included)
```python
print(b[2:5])    # Output: llo
```

Slice From the Start: starts at the first character
```python
print(b[:5])     # Output: Hello
```

Slice To the End: goes to the end of the string
```python
print(b[2:])     # Output: llo, World!
```

Negative Indexing: slice from the end of the string
Get characters from "o" (position -5) to "r" (position -2, not included)
```python
print(b[-5:-2])  # Output: orl
```



### String Concatenation
To concatenate, or combine, two strings you can use the `+` operator.

```python
# Merge variable a with variable b
a = "Hello"
b = "World"
c = a + b

# Add a space between them
c_spaced = a + " " + b
```

### Common String Methods
```python
text = "data analysis"

text.upper()      # 'DATA ANALYSIS'
text.lower()      # 'data analysis'
text.replace("data", "business") # 'business analysis'
text.split(" ")   # ['data', 'analysis']
text.strip()      # remove leading/trailing spaces
```

### Type Casting with String
Used for: data conversion during processing.

```python
# string → int
num = int("10")

# number → string
label = "Value: " + str(100)
```

### Escape Characters
To insert characters that are illegal in a string, use an escape character (`\`). 
For example, to use double quotes inside a string that is surrounded by double quotes:

```python
# The escape character (\") allows using double quotes
txt = "We are the so-called \"Vikings\" from the north."
```

**Other escape characters used in Python:**

| Code | Result |
| :--- | :--- |
| `\'` | Single Quote |
| `\\` | Backslash |
| `\n` | New Line |
| `\r` | Carriage Return |
| `\t` | Tab |
| `\b` | Backspace |
| `\f` | Form Feed |


## Data Structures

### List
Lists are used to store multiple items in a single variable. They are ordered, changeable, and allow duplicate values.

#### Common List Methods

**1. Adding Elements**
```python
fruits = ["apple", "banana"]

# append() - Adds an element at the end of the list
fruits.append("orange")
# Result: ['apple', 'banana', 'orange']

# insert() - Adds an element at the specified position (index, value)
fruits.insert(1, "mango")
# Result: ['apple', 'mango', 'banana', 'orange']

# extend() - Adds the elements of another list to the end
tropical = ["pineapple", "papaya"]
fruits.extend(tropical)
# Result: ['apple', 'mango', 'banana', 'orange', 'pineapple', 'papaya']
```

**2. Removing Elements**
```python
fruits = ['apple', 'mango', 'banana', 'orange']

# remove() - Removes the item with the specified value
fruits.remove("banana")
# Result: ['apple', 'mango', 'orange']

# pop() - Removes the element at the specified position (removes last item if no index is specified)
removed_item = fruits.pop(1)  # removes 'mango'
# Result: fruits = ['apple', 'orange'], removed_item = 'mango'

# clear() - Removes all the elements from the list
fruits.clear()
# Result: []
```

**3. Searching and Counting**
```python
nums = 

# index() - Returns the index of the first element with the specified value
pos = nums.index(30)
# Result: 2

# count() - Returns the number of elements with the specified value
cnt = nums.count(20)
# Result: 2
```

**4. Sorting and Reversing**
```python
cars = ["Ford", "BMW", "Volvo"]

# sort() - Sorts the list (alphabetically or numerically by default)
cars.sort()
# Result: ['BMW', 'Ford', 'Volvo']

# reverse() - Reverses the order of the list
cars.reverse()
# Result: ['Volvo', 'Ford', 'BMW']
```

**5. Copying**
```python
original = ["apple", "banana"]

# copy() - Returns a copy of the list (useful to prevent modifying the original list)
new_list = original.copy()
# Result: new_list is ['apple', 'banana']
```

### Tuple
A tuple is:
- ordered
- unchangeable (immutable)
- able to store duplicate values

#### Create a Tuple
```python
fruits = ("apple", "banana", "cherry")
print(fruits)
```

Difference between Tuple and list:
```python
fruits = ("apple", "banana", "cherry")
print(type(fruits))  # <class 'tuple'>

fruits = ["apple", "banana", "cherry"]
print(type(fruits))  # <class 'list'>
```


#### Tuple with One Item
To create a tuple with only one item, must add a comma after the item.

```python
one_item = ("apple",)
print(type(one_item))
```

#### Access Tuple Items
You can access tuple items by using the index number.

```python
fruits = ("apple", "banana", "cherry")

print(fruits)   # apple
print(fruits)   # banana[1]
print(fruits[-1])  # cherry
```

#### Tuple is Unchangeable
Once a tuple is created, you cannot change its values directly.

```python
fruits = ("apple", "banana", "cherry")
# fruits = "kiwi"  # This will cause an error[1]
```

#### Change Tuple Values
Since tuples are immutable, you cannot change them directly.
A common workaround is:
1. Convert the tuple to a list
2. Change the list
3. Convert it back to a tuple

```python
x = ("apple", "banana", "cherry")
y = list(x)
y = "kiwi"[1]
x = tuple(y)

print(x)  # ('apple', 'kiwi', 'cherry')
```

#### Add Items to a Tuple
Tuples do not have a built-in `append()` method, but there are two common ways to add items.

##### Method 1: Convert into a List
```python
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)

print(thistuple)
```

##### Method 2: Add Tuple to a Tuple
To add one item, create a new tuple with a trailing comma.

```python
thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y

print(thistuple)
```

#### Unpacking a Tuple
You can assign tuple values to variables.

```python
fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow)
print(red)
```

#### Using Asterisk `*`
If the number of variables is less than the number of values, you can use `*` to collect the remaining values into a list.

```python
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")

(green, yellow, *red) = fruits

print(green)   # apple
print(yellow)  # banana
print(red)     # ['cherry', 'strawberry', 'raspberry']
```

#### Why Use a Tuple?
Tuples are useful when:
- the data should not be changed
- you want to group related values together
- you need a fixed collection of items

#### Example
```python
coordinates = (51.5074, -0.1278)
print(coordinates)
```

### Set
Sets are used to store multiple items in a single variable. They are written with curly brackets `{}`.

A set is a collection which is:
- **Unordered:** Items do not have a defined order and cannot be referred to by index.
- **Unchangeable:** You cannot change items after creation (but you can add/remove items).
- **Unindexed:** No keys or index numbers.

#### Create a Set
```python
thisset = {"apple", "banana", "cherry"}
print(thisset)
# Output: {'banana', 'cherry', 'apple'} (Order may vary!)

# Using the set() constructor
thisset = set(("apple", "banana", "cherry")) # note the double round-brackets
```

#### Duplicates Not Allowed
Sets cannot have two items with the same value. Duplicate values will simply be ignored.

```python
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)
# Output: {'banana', 'cherry', 'apple'}
```

*Note on Boolean and Integer equivalence in Sets:*
- `True` and `1` are considered the same value.
- `False` and `0` are considered the same value.

```python
set_true = {"apple", "banana", "cherry", True, 1, 2}
print(set_true)
# Output: {True, 2, 'banana', 'cherry', 'apple'}

set_false = {"apple", "banana", "cherry", False, True, 0}
print(set_false)
# Output: {False, True, 'banana', 'cherry', 'apple'}
```

#### Get Length and Data Types
Set items can be of any data type (String, int, boolean) and can contain different data types in the same set.

```python
thisset = {"apple", "banana", "cherry"}
print(len(thisset))
# Output: 3

set_mixed = {"abc", 34, True, 40, "male"}
print(type(set_mixed))
# Output: <class 'set'>
```

#### Adding Items
Once a set is created, you cannot change its items, but you can add new items.

```python
thisset = {"apple", "banana", "cherry"}

# add() - Add one item
thisset.add("orange")
print(thisset)
# Output: {'banana', 'orange', 'cherry', 'apple'}

# update() - Add items from another set (or any iterable like list, tuple)
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)
# Output: {'banana', 'orange', 'cherry', 'pineapple', 'apple', 'papaya', 'mango'}

# Add elements of a list to a set
mylist = ["kiwi", "grape"]
thisset.update(mylist)
```

#### Removing Items
To remove an item, use `remove()` or `discard()`.

```python
thisset = {"apple", "banana", "cherry"}

# remove() - Removes specified item. Will raise an error if item doesn't exist.
thisset.remove("banana")
print(thisset)
# Output: {'cherry', 'apple'}

# discard() - Removes specified item. Will NOT raise an error if item doesn't exist.
thisset.discard("kiwi") # No error raised
```

**Other removal methods:**
```python
thisset = {"apple", "banana", "cherry"}

# pop() - Removes a random item and returns it
removed_item = thisset.pop()
print(removed_item)
# Output: 'banana' (or any other item)

# clear() - Empties the set
thisset.clear()
print(thisset)
# Output: set()

# del - Deletes the set completely
del thisset
# print(thisset) would raise an error because thisset no longer exists
```

#### frozenset
A `frozenset` is an immutable version of a set. Once created, you cannot add or remove items.

```python
# Create a frozenset from an iterable
x = frozenset({"apple", "banana", "cherry"})

print(x)
# Output: frozenset({'cherry', 'banana', 'apple'})

print(type(x))
# Output: <class 'frozenset'>
```

### Dictionary
Dictionaries are used to store data values in `key:value` pairs. They are written with curly brackets `{}`.

A dictionary is:
- **Ordered:** Items have a defined order that will not change.
- **Changeable:** You can change, add, or remove items.
- **Duplicates Not Allowed:** Cannot have two items with the same key. Duplicate values will overwrite existing values.

#### Create a Dictionary
```python
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)
# Output: {'brand': 'Ford', 'model': 'Mustang', 'year': 1964}
```

#### Accessing Items
You can access the items by referring to its key name.

```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Using square brackets
x = thisdict["model"]
print(x)  # Output: Mustang

# Using the get() method (safer, doesn't raise error if key is missing)
y = thisdict.get("model")
print(y)  # Output: Mustang
```

#### Get Keys (View Objects)
The `keys()` method returns a view of the dictionary keys. Any changes done to the dictionary will be reflected in the keys list automatically.

```python
car = {"brand": "Ford", "model": "Mustang", "year": 1964}
x = car.keys()

print(x) 
# Output: dict_keys(['brand', 'model', 'year']) (before the change)

car["color"] = "white"

print(x) 
# Output: dict_keys(['brand', 'model', 'year', 'color']) (after the change)
```

#### Change and Add Items
You can use the `update()` method to update an existing item or add a new item. The argument must be a dictionary or an iterable object with key:value pairs.

```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Update existing value
thisdict.update({"year": 2020})
print(thisdict["year"])  # Output: 2020

# Add new item
thisdict.update({"color": "red"})
print(thisdict)  
# Output: {'brand': 'Ford', 'model': 'Mustang', 'year': 2020, 'color': 'red'}
```

#### Removing Items
```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# pop() - Removes the item with the specified key name
thisdict.pop("model")
print(thisdict)  
# Output: {'brand': 'Ford', 'year': 1964}

# popitem() - Removes the last inserted item
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}
thisdict.popitem()
print(thisdict)  
# Output: {'brand': 'Ford', 'model': 'Mustang'}

# del - Removes the item with the specified key name
del thisdict["brand"]
print(thisdict)  
# Output: {'model': 'Mustang'}

# clear() - Empties the dictionary
thisdict.clear()
print(thisdict)  
# Output: {}
```

#### Loop Through a Dictionary
When looping through a dictionary, the return values are the **keys**, but there are methods to return the **values** or **both**.

```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Print all keys
for x in thisdict:
    print(x)
# Output: brand \n model \n year

# Print all values using keys
for x in thisdict:
    print(thisdict[x])
# Output: Ford \n Mustang \n 1964

# Print all values using values() method
for x in thisdict.values():
    print(x)
# Output: Ford \n Mustang \n 1964

# Loop through both keys and values using items() method
for x, y in thisdict.items():
    print(x, y)
# Output: 
# brand Ford 
# model Mustang 
# year 1964
```

#### Nested Dictionaries
A dictionary can contain other dictionaries.

```python
# Create a dictionary containing three dictionaries
myfamily = {
  "child1" : {"name" : "Emil", "year" : 2004},
  "child2" : {"name" : "Tobias", "year" : 2007},
  "child3" : {"name" : "Linus", "year" : 2011}
}

# Access Items in Nested Dictionaries
print(myfamily["child2"]["name"])
# Output: Tobias

# Loop Through Nested Dictionaries
for x, obj in myfamily.items():
    print(x)
    for y in obj:
        print(y + ':', obj[y])
        
# Output:
# child1
# name: Emil
# year: 2004
# child2
# name: Tobias
# year: 2007
# child3
# name: Linus
# year: 2011
```

### Summary: Built-in Data Structures Comparison

| Data Structure | Brackets | Ordered | Changeable (Mutable) | Allows Duplicate Values | Indexed |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **List** | `[ ]` | Yes | Yes | Yes | Yes |
| **Tuple** | `( )` | Yes | No | Yes | Yes |
| **Set** | `{ }` | No | No* (can add/remove) | No | No |
| **Dictionary** | `{key: value}` | Yes | Yes | No (Keys) / Yes (Values) | Yes (by Key) |


## Functions

### Creating a Function
In Python, a function is defined using the `def` keyword, followed by a function name and parentheses.

```python
def my_function():
    print("Hello from a function")

# Calling the function
my_function()
# Output: Hello from a function
```

### Arbitrary Arguments (`*args`)
The `*args` parameter allows a function to accept any number of positional arguments. Inside the function, `args` becomes a **tuple** containing all the passed arguments.

```python
def my_function(*args):
    print("Type:", type(args))
    print("First argument:", args)
    print("Second argument:", args)[1]
    print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")

# Output:
# Type: <class 'tuple'>
# First argument: Emil
# Second argument: Tobias
# All arguments: ('Emil', 'Tobias', 'Linus')
```

### Lambda Functions
A lambda function is a small anonymous function. It can take any number of arguments, but can only have **one expression**. It is frequently used in data analysis (e.g., inside pandas `apply()` methods).

```python
# Example 1: Add 10 to argument a
x = lambda a : a + 10
print(x(5))
# Output: 15

# Example 2: Multiply argument a with argument b
y = lambda a, b : a * b
print(y(5, 6))
# Output: 30

# Example 3: Summarize argument a, b, and c
z = lambda a, b, c : a + b + c
print(z(5, 6, 2))
# Output: 13
```

### Generators and the `yield` Keyword
Generators are functions that can pause and resume their execution. The `yield` keyword is what makes a function a generator.

When a generator function is called, it returns a **generator object** (an iterator). The code inside the function does not execute immediately; it only executes when you iterate over the generator. 

When `yield` is encountered, the function's state is saved, and the value is returned. The next time the generator is called, it continues from exactly where it left off. This is highly memory-efficient for processing large datasets.

```python
# Example 1: A simple generator function
def my_generator():
    yield 1
    yield 2
    yield 3

for value in my_generator():
    print(value)
# Output: 
# 1
# 2
# 3

# Example 2: Generator that yields numbers up to n
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

for num in count_up_to(5):
    print(num)
# Output:
# 1
# 2
# 3
# 4
# 5
```

