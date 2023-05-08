Title: Arbitrary File Read/Write to RCE
Date: 2023-05-07 22:00
Category: Linux
Tags: ctf, umdctf2023, proc_self_mem, arbitrary_file_read_write, rust
Status: draft

During UMDCTF 2023, I encountered an intriguing pwn-challenge authored by Triacontakai. The application was written in Rust and seemed perplexing, as it didn't use any unsafe keywords. Initially, we expected the flag to be located next to the application, and with knowledge of a path-traversal and file read/write primitive, we believed it would be a simple task to read the flag.

However, after the CTF had ended, I spoke with the creator of the challenge, and he provided me with an exploit that utilized /proc/self/mem to create Remote Code Execution (RCE).

The lessons are quite interesting, so I will go trough the application and the exploit and what we can learn about to exploit hopefully any given application on Linux where we have an arbitrary file read/write.

First, let me provide u with the challenge, so u can look for urself:


