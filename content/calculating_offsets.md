Title: De Bruijn Pattern: A Method for Calculating Offsets and the Tools of Trade
Date: 2023-05-07 22:00
Category: General
Tags: offset, brujin, debrujin

## Intro

In the field of binary exploitation, it is a common occurrence to have to determine the offset of our input to a program. In early buffer overflow exploits, a large buffer of repeating characters such as "A" * 400 was often used. However, when overwriting the instruction pointer, the exact location of the overwrite was unknown.

To address this issue, the technique of using ever-changing patterns was introduced. For example, a pattern like "...AAACAAADAAAE..." could be used.
By finding the location of the instruction pointer in the pattern (imagine it pointing to "AAAD"), the offset of the input could be determined. 
But the de bruijn pattern is even better as you might think by just this example. Because it can also give you the offset of pointing to "AADA" or "ADAA" or "DAAA", since each of this sub-parts are also unique. So any offset into the input pattern can be precisely determined.
This technique remains an important tool in modern binary exploitation.

## Tools

There are many tools available to create such patterns and calculate offsets in binary exploitation. However, I have some opinions and tips I'd like to share.

One commonly used tool is the Metasploit Framework, which includes the msf-pattern-create and msf-pattern-offset commands:

```bash
msf-pattern-create -l <length>

msf-pattern-offset -q <pattern>
```

Although this tool is well-known and recommended by many, I personally do not prefer it due to its clunkiness and difficulty of use on Windows. Additionally, it can be flagged by antivirus software, causing additional problems.

For these reasons, I prefer to use radare2 and its ragg2 tool, which works well on Windows, Linux, and Mac:

```bash
ragg2 -P <length> -r

ragg2 -P <length> -q <offset> # offset as 0x....
```

One limitation of ragg2 is that it can only create one pattern with a predefined alphabet. This limitation can be problematic when working with input buffers that contain so-called "bad characters" that the target program does not handle correctly.

An alternative tool to overcome this limitation is pwntools pwnlib. Although its usage requires coding, it is very simple and can easily be accomplished with a few lines of code:

```python
from pwn import *

# Define your custom alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Generate a cyclic pattern with a length of 200 using the custom alphabet
pattern = cyclic(200, alphabet)

print(pattern)

# Find the offset of a later specified value in the pattern
offset = cyclic_find('mnaa', alphabet)

# Print the offset
print(f'Offset: {offset}')
```

It's worth noting that Metasploit's pattern-create command does have an option (-s) for specifying a custom alphabet.

Other tools such as mona.py (Python2) or PEDA (only for GDB) are also available. However, they each have limitations that make me hesitant to include them in my general toolset.


## Alphabets in patterns 

Lets think about the alphabets for a second. In case we have a limitation and we want to switch to other characters, just how many would we need for creating a fitting buffer?

The chars in these patterns are normaly a byte wide, which means on a 32-bit system 4 chars will be filling 1 register.
So we have alphabet size ^ 4.

This comes down to
```
2  chars = 16    maximal buffer length
5  chars = 625   maximal buffer length
10 chars = 10000 maximal buffer length
```
On 64-bit systems its even easier, since it will be alphabet size ^ 8
