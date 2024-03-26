Title: WDM Driver Identification - 
Date: 2024-03-11 18:00
Category: windows
Tags: windows, reversing, driver, fuzzing
Status: draft

## Background Story

Since I am looking into having a setup for fuzzing for windows components. One of my first target is windows drivers. While I can identify these componentes with my previously pe-extraction code in memflow, yes drivers are PE files, I now need a way to analyse them automatically.

## Initial thoughts

I guess a good starting spot is to look for drivers using a buffer from usermode. These can be made with IRP [IRP](https://learn.microsoft.com/de-de/windows-hardware/drivers/ddi/wdm/ns-wdm-_irp) which are part of [WDM-Drivers](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/types-of-wdm-drivers).

So we need to:

1) Identify drivers which are WDM-Drivers
2) Find the IRP Requests
3) Identify the IRP-Request for accepting usermode buffers

### Identifying drivers

When looking at a driver in ghidra, there is a set of imports from the ntoskrnl.exe

Here we can identify if a driver uses functions from the wdm.h. Common functions are named IoCreate... IoDelete...

For example when looking at the HEVD Driver, we can see this imports:
![Symbol tree HEVD](images\ghidra_symbols.png)

We could make a list from WDM.h to look for all applicable functions, but I have a shortcut in mind. 

We need to be able to interact with the driver in the end. Therefore it needs to register a device in the system.
For now I am sure that IoCreateDevice and IoCreateSymbolicLink are enough to identify the usage of WDM in a meaningful way.

### Finding the IRP-Requests

So lets start thinking about it. Lots of drivers will have a DispatchRoutine, which will list all the functions something could call the driver with. But DispatchRoutines are not needed. They are optional.