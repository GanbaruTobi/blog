Title: Understanding Python f-Strings for RCE, Part 1
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
![Result](./images/executed.png)

and

```python
tmp = "print(1234)"
print(f"This is not: {tmp}")
```

![Execure and Not](./images/execudandnot.png)

This might look very close to each other, but it seems python sees differences in it.
Before going on, we need to understand differences, before trying more techniques.

## Python under the Hood

To display the bytecode (disassembly) of a function in Python, you can use the dis module. The dis module provides a disassembler for Python bytecode, allowing you to inspect the low-level instructions executed by the Python interpreter.

Lets do this for a new-style f-string:
![dis execution](./images/disone.png)

What we can see here is that test0 is not a string constant, but being evaluated at runtime. Now this sounds like an eval() code, but lets do some thats to show u that its not so easy:

```python
import dis

def test1():
    tmp = print(1234)
    f"This is executed: {tmp}"

def test2():
    tmp = "print(1234)"
    f"This is not: {tmp}"

dis.dis(test1)
test1()
print("----- between -----")

dis.dis(test2)
test2()
```
![dis execution](././images/disexec3.png)

In test one we can see the print being executed, but don't get mislead here, its already executed in the variable declaration line. The vaulue stored in tmp is null and therefore out execution evaluation is done on nothing (but its executed).

In the second example tmp is just formatted, no call happens.

If we want to have a way to execute code from something like f" Exec {user-input}", we need a way to provide something thats not just seen as a string (LOAD CONST).


### Further tests

We need to bind something to a variable that is being seen as a function or something that would have some hidden code executed. I could imagine two ways to do this. With a lambda function or with a class.
The problem with lamda is, that it defines tmp as a function, and the function call would need tmp()

```python
tmp = lambda: print(1234)
print(f"This is not: {tmp}")

tmp = lambda: print(1234)
print(f"This is : {tmp()}")
```

![lambda exec](././images/lambda2.png)
So we are not abe to place something executeable into an variable with this directly. But we can define a function call... no we cannot. The call is not part of the string evaluation, as we have seen in the beginning.

With a class, we can try something, but it is clear that instantiation leads to to same problems as before.
```python
class MyClass:
    def __init__(self):
        self.message = "Hello, World!"

tmp = MyClass 
print(f"This is : {tmp}")
print(f"This is : {tmp()}")
```

## Exploitable Case

Just like [here](https://security.stackexchange.com/questions/238338/are-there-any-security-concerns-to-using-python-f-strings-with-user-input) it is possible to exploit, but where is the difference in that example?

The example:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

secret = 'abc123'

class Handler(BaseHTTPRequestHandler):
    name = 'funtimes'
    msg = 'welcome to {site.name}'
    def do_GET(self):
        res = ('<title>' + self.path + '</title>\n' + self.msg).format(site=self)
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(res.encode())

HTTPServer(('localhost', 8888), Handler).serve_forever()
```

The difference is that the attack actually controls the string that is going to be formatted.
So this line:

```python
res = ('<title>' + self.path + '</title>\n' + self.msg).format(site=self)
```
will be made into something we directly control, in the example to

```python
res = ('<title>' + 'XXX{site.do_GET.__globals__[secret]}' + '</title>\n' + self.msg).format(site=self)
```

Since from the example ppl also discussed if the vulnerabe is a RCE, lets look at what we see.
We control the left part, but its being formated on the condition set in the right part. So the code
expects and wont run without exactly 1 pair of {} and it want to format the site variable with the self value.
So the code will load 'self' into 'site' and then evaluate the code. In the case of this code, this gives us full control ob the Handler instance and we allready know by the provided solution that its possible to access members.

Python has lots of magic functionality, but thats something we will look at in a follow up post

## Conclusion

It seems that there needs to be special cases, in which formatting leads to exploitable evaluation. So I would think about it that way. If the user-Input is parsed/manipulated one time, its probably save and if there are two manipulations it might create a needed side-effect.

Even in the case of having such a side-effect, we are unsure if its enough for an full RCE. So we will keep on looking in part 2.