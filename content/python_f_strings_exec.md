Title: Understanding Python f-Strings for RCE
Date: 2023-06-15 22:00
Category: Rev
Tags: Python, Eval, f-Strings

## What are Python f-Strings

Python f-strings, short for "formatted string literals," are a convenient way to embed expressions inside string literals, allowing for easy string interpolation. F-strings were introduced in Python 3.6 and provide a concise and readable syntax for creating formatted strings.

To create an f-string, you prefix the string literal with the letter "f" or "F" and enclose expressions inside curly braces {}. The expressions inside the curly braces are evaluated at runtime and their values are inserted into the resulting string. Here's an example:

```python
name = "Alice"
age = 25

# Using f-string to create a formatted string
message = f"My name is {name} and I'm {age} years old."
print(message)
```

## Why write about it?

Well, every now and then, we pass by this functions in source code and discuss if its a way for RCE or not.
There are links on the internet [1](https://www.geeksforgeeks.org/vulnerability-in-str-format-in-python/), [2](https://github.com/adeptex/CTF/blob/master/fstring-injection.md), ..., claiming exploitabilty and [others](https://security.stackexchange.com/questions/238338/are-there-any-security-concerns-to-using-python-f-strings-with-user-input) show its often not.

## Example Code

So lets review some snippets to see about the confusions.

```python
print(f"This is executed: {print(1234)}")
```
![Result](../images/executed.png)

and

```python
tmp = "print(1234)"
print(f"This is not: {tmp}")
```

[Execure and Not](../images/execudandnot.png)

This might look very close to each other, but it seems python sees differences in it.
Before going on, we need to understand differences, before trying more techniques.

## Python under the Hood

To display the bytecode (disassembly) of a function in Python, you can use the dis module. The dis module provides a disassembler for Python bytecode, allowing you to inspect the low-level instructions executed by the Python interpreter. Lets do this for our two examples:

```python
import dis

def test1():
    print(f"This is executed: {print(1234)}")

def test2():
    tmp = "print(1234)"
    print(f"This is not: {tmp}")

dis.dis(test1)
print("----- between -----")
dis.dis(test2)
```
![dis execution](../images/disexec.png)


Some might argue that the second example is a string and therefore not getting evaluated.
Thats why we try bind the function directly and also use a lambda, which would be a way to do it i guess.

```python
tmp = print(1234)
print(f"This is not: {tmp}")
```

```python
tmp = lambda: print(1234)
print(f"This is not: {tmp}")
```
