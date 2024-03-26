Title: Fuzzing for Windows (6) - Working with libAFL
Date: 2024-03-19 13:00
Category: windows
Tags: windows, fuzzing
Status: draft

## Whats the goal

Understanding the parts a fuzzer is build of in libAFL. Especially for qemu systemmode and frida, since these enable us to fuzz blackbox binaries. Nyx also is possible here, but I will leave out for now, because we will need a modified host to use it.

## What parts of LibAFL can we use on Windows

Right now the meaningfull options are to compile a target with instrumentation or use frida, nyx, or qemu. Here are example fuzzers that use these techniques.

- [LibAFL](https://github.com/AFLplusplus/LibAFL)
    - [LibAFL-Windows](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/libfuzzer_windows_asan)
    - [LibAFL-frida](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/frida_gdiplus)
    - [LibAFL-nyx](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/nyx_libxml2_parallel)
    - [LibAFL-Qemu (Systemmode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_systemmode)
    - [LibAFL-Qemu (Usermode)](https://github.com/AFLplusplus/LibAFL/tree/main/fuzzers/qemu_coverage)

## Generating Docs

```bash
cargo docs --open 
```

With this command we can generate the docs of the project. Also of the modules that we want to use, we can cd into the modules and build docs from there only too
The modules we use are reachable here:

- [LibAFL-frida](https://github.com/AFLplusplus/LibAFL/tree/main/libafl_frida)
- [LibAFL-nyx](https://github.com/AFLplusplus/LibAFL/tree/main/libafl_nyx)
- [LibAFL-Qemu](https://github.com/AFLplusplus/LibAFL/tree/main/libafl_qemu)

## Further Resources

There is [this](https://epi052.gitlab.io/notes-to-self/blog/) series about building some fuzzers. The WIP Book about libAFL is [here](https://aflplus.plus/libafl-book).

Than there is a [workshop](https://www.atredis.com/blog/2023/12/4/a-libafl-introductory-workshop) available.


## General Components 

### Observation Channel - Observer

The Observer is the component in which we track what happens in the target. In AFL this would be the coverage map for example.
Another Observer could be to track execution time, or we could introduce custome code points in a binary and track those.

### Target Execution - Executor

The Executor is the component dealing with how to run the target. This can be a binary or a VM or other stuff.

For example there is an in-memory Executor. This is known as the LLVMFuzzOneInput() Function in harnesses. This function is exported and can be called by a fuzzer. Therefore the fuzzing loop is inside an application.

Another Executor would be a forkserver. The process is forked (copied) and executed with new fuzzer input each time.

The Executor also connects the Observer with the target.

### Understanding the Target - Feedback

The Feedback Modul is to filter the Observator for interesting results.

For example finding observations with new coverage. Or look for bigger memory allocations. 

Also there is Objectives

#### Objective Feedback

This are goals we give our fuzzing campaign, like finding crashes.

Another goal would be to reach a certain point in the program, think of login-bypasses.

### Input

Of course we have to use something to feed to the program.
It does not have to be an expected format, but it has to be a structure that can be manipulated.

### Corpus

Storage of the interesting Inputs and Metadata we found with Feedback. This will be used by the fuzzer if neccessary.
It also measures how they relate to each other (think duplicates and stuff).

This can be implemented as a queue for example (AFL)


### RNG - Random Number

Important what to use for random stuff, since the performance depends on it.

### State

All the evolving parts when fuzzing.
Like corpus and feedback.

### Events and Event Manager

Events can be a new coverage, or a crash , or something important...

An naive Event Manager just logs this to output.


### libAFL-frida

For now this module only supports x86_x64, so we cannot fuzz x86 targets. Also officialy it only is able to fuzz libraries.

Maybe we are able to foul the fuzzer to accept an exe that has been converted into an dll.
Like it is done [here](https://github.com/hasherezade/dll_to_exe).

### libAFL-qemu

To understand the qemu module its hard to just go by the docs, bc they are kind of empty.

But there is [this](https://s3.eurecom.fr/docs/bar24_malmain.pdf) paper describing the design.

Also there is a windows fuzzer released with the paper in this [repo](https://github.com/AFLplusplus/libafl_qemu_artifacts). But its currently not building.