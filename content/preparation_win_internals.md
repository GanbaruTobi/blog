Title: Preparing for Windows Internals for Security Engineers
Date: 2023-05-08 13:00
Category: Windows
Tags: OffensiveCon, Windows Internals, Yarden Shafir,

In mid of May I have the honor to participate in the Windows Internals 4-day training at OffensiveCon. Since I want to come prepared there are some things I will do beforehand. For anyone else going for the training or wanting to check out its topics this might come in handy.

## General Preperation

I will go with a split process of reading the new Windows Internals Books and watching the videos on Plural Sight to Windows 11 from Pavel Yosifovich (payed content). They both have the same topic, the books have more depth, but are somewhat harder and more time consuming to go through.

The videos are very good, but sometimes lack on a certain topic. Everytime one option gets boring or I find myself not progressing I switch to the other method.

## Specific Preperation

After that I go trough the description of the training and on every buzzword I don't know of, I will research about the contents.

The buzzwords per OS version are:

Windows 11:

1. GRU bootkits 
1. PLA software supply chain implants
1. NSA Backdoors
1. Kernel Data Protection (KDP)
1. eXtended Control Flow Guard (XFG)
1. Kernel Control-flow Enforcement Technology (KCET)
1. System Guard Runtime Assertions
1. Secure Launch framework (Intel TXT and AMD SKINIT for new DRTM-based attestation)

Windows 10:

1. Virtual Trust Levels (VTL)
1. Virtualization Based Security (VBS)
1. Hyper Visor Code Integrity (HVCI)
1. Kernel Control Flow Guard (KCFG)
1. Software Guard Extensions (SGX)

Windows 8.1:

1. Protected Process Light
1. Custome Code Signing Policies

Windows 8:

1. AppContainer
1. Secure Boot


Windows 7:

1. Object Manager data structures


### Resources to the Topics

<span style="color:blue">GRU Rootkits</span> seems to be made up or at least I can't find anything about it. I guess GRU is something russian... or the (good) villain from minions. Anyway, its a rootkit and therefore just a kernel malware.

Sadly again, no idea what <span style="color:blue">PLA</span> stands for. But its about supply chain attacks. I don't see how preparation for that would help me for the course.

<span style="color:blue">NSA Backdoors</span> is at least something known. So the text goes on to describe the above three as kernel and firmware malware.

My understanding is its about modified kernels or drivers.
Therefore preparing would be to learn about offensive driver development (they run in the kernel). I took the course from [here](https://training.zeropointsecurity.co.uk/courses/offensive-driver-development).

Also there is a book from Pavel about Windows Kernel Programming, which I will go through.

Next we have <span style="color:blue">Kernel Data Protection (KDP)</span>. It is explained [here](https://www.microsoft.com/en-us/security/blog/2020/07/08/introducing-kernel-data-protection-a-new-platform-security-technology-for-preventing-data-corruption/). It is a mechanism to mark parts of kernel and driver as read only data. A copy or other way of attestation of the data is hold in the hypervisor through VBS (read on for VBS).

For <span style="color:blue">eXtended Control Flow Guard (XFG)</span> a good start is [here](https://connormcgarr.github.io/examining-xfg/), followed with [that](https://www.offsec.com/offsec/extended-flow-guard/).

The <span style="color:blue">Kernel Control-flow Enforcement Technology (KCET)</span> seems to be very new. I just read about normal CET [here](https://windows-internals.com/cet-on-windows/) to get a basic understanding.
It uses a "Shadow Stack" which holds a copy of all return addresses used by the program. That way its not possible to overwrite the return address of a function without being noticed. I would assume that a shadow stack in a hypervisor will do the same for the kernel.

<span style="color:blue">System Guard Runtime Attestation</span> is written about [here](https://www.microsoft.com/en-us/security/blog/2018/04/19/introducing-windows-defender-system-guard-runtime-attestation/)  

<span style="color:blue">Secure Launch framework</span> seems to be for secure boot.
I am not interested so much, but [here](https://community.amd.com/t5/business/amd-and-microsoft-secured-core-pc/ba-p/418204) is good information.

From here on everything is in the Windows Internals Books, which should be a very good reference.



