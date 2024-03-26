Title: Fuzzing for Windows (1) - First Thoughts and Fuzzer Selection
Date: 2024-02-20 13:00
Category: windows, fuzzing
Tags: windows, fuzzing

## Whats the goal

We want to find the best multi-purpose fuzzers which are state-of-the-art. They are supposed to run inside of Windows or work with Windows VMs as targets.

## Initial Selection

The fuzzers I found which are worth having a look at are:

- [WinAFL](https://github.com/googleprojectzero/winafl)
- [Winnie](https://github.com/sslab-gatech/winnie)
- [Jackalope](https://github.com/googleprojectzero/Jackalope)
- [nyx](https://github.com/nyx-fuzz)
- [msfuzz](https://github.com/0dayResearchLab/msFuzz)
- [What the fuzz](https://github.com/0vercl0k/wtf)
- [LibAFL](https://github.com/AFLplusplus/LibAFL)
    - [LibAFL-Windows](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/libfuzzer_windows_asan)
    - [LibAFL-frida](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/frida_gdiplus)
    - [LibAFL-nyx](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/nyx_libxml2_parallel)
    - [LibAFL-Qemu (Systemmode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_systemmode)
    - [LibAFL-Qemu (Usermode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_coverage)

## Overview

The selection hold different kind of fuzzers which will operate on user mode or kernel mode. Since on Windows it is more common to not hold the source code of targets, so most of these fuzzers will have a way to intrument binaries without source-code. 

Else, we are using at least coverage-guided fuzzers. Some will be snapshot fuzzers, which will allow us to hold a bit of state more.

We lack capabilities for anything of complex states, so fuzzing a protocol, for example, is not directly solveable with this basis. It's achievable with more development (but a hard task). I recommend if u want to follow along, that u open all the fuzzers' pages and see if you come to the same conclusions as I do. This is just a fast look over for now. After we have some initial choosings, we will look deeper into the features.

## WinAFL

Since the original AFL is designed for Unix systems, this is a version that achieves instrumentation through these four methods:

- Dynamic instrumentation using DynamoRIO (http://dynamorio.org/)
- Dynamic instrumentation using TinyInst (https://github.com/googleprojectzero/TinyInst)
- Hardware tracing using Intel PT
- Static instrumentation via Syzygy

DynamoRIO is able to do instrumentation very well, but can be complex to setup. TinyInst is only able to do minimal instrumentation but is easy to setup. I did not use Intel PT yet, but it will need a (modern) Intel CPU.
[Syzygy](https://github.com/google/syzygy) is archived and therefore I will not even consider it.

Else the code-base is antique, its many years old with little updates, most of the code is between 2 and 7 years old. I am sure its not worth considering because the speed and functionaly with other tools should be way better.

## Winnie

Winnie is developed on top of the basis WinAFL gives. It is able to create something comparable to a fork() to drastically improve useability. But still this code is old (3 years) and is only tested against one fixed version of windows. 

Therefore I have nothing to say besides we will probably skip over this fuzzer too.

## Jackalope

The Jackalope fuzzer works with TinyInst and therefore is able to do basic (blackbox) binary instrumentation. It also sees close to no development, last commit is 8 months old, and therefore is just a bit better than the previous options.
It allows for parallel fuzzing and has a grammar mutator.

I still believe we can do better and this probably won't come out to be a real option.

## kAFL

The actively maintaned kAFL is a fuzzer coming directly from Intel it seems. Therefore instrumentation/tracing is done with Intel PT.
Other than that is seems to have many features and claims to be able to fuzz user and kernel mode on Windows.

It works by instrumenting VMs based on QEMU/KVM. It also seems to support nesting, which would allow hypervisor-fuzzing probably. On the other hand having to run QEMU for userland fuzzing means to have an unwanted ressource cost. For kernel this is probably pretty optimal for us. Else they have an example for windows user and kernel mode fuzzing [here](https://intellabs.github.io/kAFL/tutorials/windows/index.html).

It needs a linux host system with a modified kernel.

It incoporates nyx which we will look at next.

## nyx-fuzz

Now we come to our first actively maintained framework/fuzzer. Nyx is a framework that allows to snapshot QEMU VMs, while nyx is acting as a hypervisor, and also provides a way for the instrumentation. Meaning the fuzzer can hold a state of an input and keep going from there not having to go through all of the programm-steps with every iteration.
This leads to having very good speeds with complex targets.
 
As meantioned before nyx is ?now? also part of kAFL.
In the terminology of nyx: nyx is the backend (handler of target) and kAFL (fuzzer) is a frontend. 

nyx also brings its own fuzzer Spec-Fuzzer, which seems to work with some kind of specification files, which is probably nothing I would like to work with. Also on first glance I didn't see any documentation, so will skip for now and only come back if neccessary.

Another nyx frontend is also accessible over LibAFL, we will talk later about LibAFL soon!

## msFuzz

msFuzz builds on top of nyx/kAFL and therefore will work with Intel PT and QEMU. The host has to be Linux. Sadly the documentation about the internals is in some Asian language.
Whats clear is that this fuzzer is designed for Drivers using IOCTL, a common communication point between user and kernel mode. This is something we surely want to fuzz.

They seem to use angr, which is for symbolic execution. angr should be a rather inperformant choice here, but often fuzzers don't realy have any working or an next to impossible to build symex solution. So I see it as an feature to have.

It seems actively maintained for now. This fuzzer will land on my nice to have list.

## What the fuzz

wtf is realy something. Since the other incorporate lots of work from each other, wtf seems to be a fuzzer build from ground up. It runs on Windows and Linux, it supports three types of execution environments (bochscpu, Hyper-V, KVM). It has coverage-guidance and snapshot-fuzzing. It brings some tools for triaging.
What is unclear for me is if it brings ASan or other memory sanitizers, or if it just will act upon a crash.

The initial setup process is described as being some work. But this fuzzer seems like a realy good starting ground for user and kernelmode fuzzing of most of the things. It is actively maintained and the development process is documented as are some fuzzing cases.

## LibALF

LibAFL is a huge deal realy. It is also a framework, coming from the developers of AFL++. Since years of experience and a huge community goes into this project it is the most feature-rich out there probably. LibAFL brings components to stick fuzzers together. Therefore we can do whitebox/blackbox, we can instrument with TinyInst, QEMU, frida, ...

The downside in my eye is that they do alot and therefore often details are not clear. Documentation is minimal. I often build fuzzer from there examples and fail in the process, because something on another used component changed or the tooling is not described well, or, or ,or ...

Therefore its a gamble if we have strikt time restrictions. But if we are able to wait some days, tickets are probably looked at and problems are resolved or at least some context is given.

We have all we wish for, but we would have to stick fuzzers together our selfs.
Lets go through some possible ways to use this.

### LibAFL-Windows

Not an officialy name, LibAFL supports building fuzzer for windows in some way. Its not tested as much, but fuzzers can be build. So seeing a fuzzer in the examples named [libfuzzer_windows_asan](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/libfuzzer_windows_asan) seems like something to build. Sadly it did not build, but I went to the fuzzing discord and other people helped me resolve the problems. Building some other fuzzer worked, some didn't. So this could be used at least for whitebox fuzzing with some work.

### LibAFL-frida

Injecting frida into processes will allow us to fuzz a good amount of software with relatively no work. This will only work for usermode is my guess. Else frida might fail for hard to track reasons and my experience with other frida-fuzzer lead me to believe that its not very reliable. Especially I am unsure about the amount of development going into frida for windows. [Here](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/frida_gdiplus) is an example fuzzer. The work is super new, so I expect bugs but lets see.
Since AFL++ had memory sanitizer for frida, I think they made that happen again. This could be a useful tool for us if tests show it's working.

### LibAFl-nyx

As talked about before, LibAFL can be a frontend for nyx. Therefore we can do snapshot-fuzzing with QEMU. [Here](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/nyx_libxml2_parallel) is an example fuzzer.

### LibAFL-Qemu

LibAFL wants to bring their own QEMU-mode. This will use QEMU in its Emulator mode, not like nyx as a virtual machine. This will allow for way better coverage, but at a cost of speed. The community makes quite the effort to make it happen. [Here is a CCC-Talk about it](https://media.ccc.de/v/37c3-12102-fuzz_everything_everywhere_all_at_once/oembed)

So there is two modes for now, [LibAFL-Qemu (Usermode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_coverage) and [LibAFL-Qemu (Systemmode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_systemmode). The Systemmode is still not released, but should come soon.

### Conclusion

There is way less good variety as I expected but we will go on with looking into nyx/kafl, msFuzz, wtf, LibAFL. I think WinAFL, Winnie and Jackalope are all superseded by LibAFL easily.

This means we have just one and a half option to run on windows (wtf, LibAFL) and three fuzzers will work with snapshot-fuzzing. With LibAFL, we have great tooling at our hand, but we don't get a great generic fuzzer gifted, we will have to build it together still.
