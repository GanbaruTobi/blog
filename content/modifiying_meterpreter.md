Title: Modifying Meterpreter to bypass AV in Source
Date: 2023-06-08 22:00
Category: Red
Tags: Metasploit, Meterpreter, AV-Bypass, Windows, Defender
Status: draft

## Whats the goal

I want to bypass Windows Defender's behaviour analysis. Therefore I try to modify a stageless meterpreter. Since I don't know about a way to analyse the runtime, I will try to modify behaviour, but also look for general things that are spottet by an unobfuscated meterpreter.

## Where is the source?

You can find the shellcodes under the following path:
```
metasploit-framework\embedded\framework\external\source\shellcode
```
but the meterpreter code is in a seperate place and this is how to setup correctly:
```
git clone https://github.com/rapid7/metasploit-payloads
cd metasploit-payloads
git submodule init
git submodule update
```

In the VS Installer we need the component "C++ Windows XP Support for VS 2017 (v141) tools [Deprecated]".After installation we went over to Visual Studio (I use 2022) and open the project from
```
metasploit-payloads\c\meterpreter\workspace
```

