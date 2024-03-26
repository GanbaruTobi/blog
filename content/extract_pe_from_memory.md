Title: Extraction of Portable Executeables (PE) from memory.
Date: 2024-03-08 10:00
Category: windows
Tags: windows, fuzzing
Status: draft

## Background Story

While developing my tools for Windows Fuzzing I wante to test out [memflow](https://github.com/memflow/memflow) for memory introspection of a running or saved VM (coredump). This could be super handy with snapshot-fuzzing, because maybe we can do all besides fuzzing with memflow, or at least I hoped it could work like that.

Soon I had to realize that I can access running programs but I lack to access the underlaying PE from memory, because the running PE is "malformed" compared to a disk file.
There are two main reasons. The sections being mapped into memory is moving them to other locations. And the memory alignmend is on a page boundary(4096 mostly on Windows), while disk alingmend follows other rules.

## What to do

Memflow is written in rust or is accessible over memflow-py in python.

For rust exists two crates [pelite](https://github.com/CasualX/pelite) and [goblin](https://github.com/m4b/goblin), which can parse the PE file format even from memory. So we would just have to fix the two problems we have.

Luckily there are other tools which already are able to work with PE memdumps, like (pe-bear)(https://github.com/hasherezade/pe-bear). So if we get stuck we can look at their source code.

##