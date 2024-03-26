Title: Nyxing thy System
Date: 2024-03-26 13:00
Category: Fuzzing
Tags: fuzzing

Since I am running my own arch OS, but still need capabilities for fuzzing with nyx, I see myself booting a Ubuntu System from an external drive. I wanted to fix this, so my friend manolis looked into getting the kernel to run on my Arch system.

## Ubuntu to Arch Kernel

Our way is to download any prebuild nyx-kernel. For example from msFuzz [nyx-6.0.0](https://github.com/IntelLabs/kafl.linux/releases/download/kvm-nyx-v6.0/linux-image-6.0.0-nyx+_6.0.0-nyx+-1_amd64.deb) or from nyx-fuzz [nyx-5.10.73](https://github.com/nyx-fuzz/KVM-Nyx/releases/tag/v5.10.73-1.2).

I will go with the nyx-fuzz one for now. I download the kernel and make a new dir ubuntu_kernel.
 
![picture 1](../images/5dde4bc256ce077a06bf5c773c35dbd4387ec22c21136dd51acf0a8443df6427.png)  

Now we place the kernel and modules into our system. 

```bash
cd ubuntu_kernel
cp ubuntu-kernel-5.10.75.zip ubuntu-kernel-5.10.75.zip
unzip ubuntu-kernel-5.10.75.zip

mkdir kernel
cd kernel
ar x ../linux-image-unsigned-5.10.75-051075-generic_5.10.75-051075.202110201038_amd64.deb
tar -xvf data.tar.xz
sudo cp boot/vmlinuz-5.10.75-051075-generic /boot/
cd ..

mkdir modules
cd modules
ar x ../linux-modules-5.10.75-051075-generic_5.10.75-051075.202110201038_amd64.deb
sudo cp -r ./lib/modules/5.10.75-051075-generic /usr/lib/modules/
```

After that we have the files in place but we have to create an initramfs. We can do so with mkinitfcpio, lets make a new preset for nyx.

```bash
sudo cp /etc/mkinitcpio.d/linux.preset /etc/mkinitcpio.d/nyx.preset
```

Now edit to the new kernel

![picture 2](../images/23928f597eba2de67a78165254c54bde2b99c7eb8b920cbc36ac2576a2fd0e48.png)  

and finish up with this

```bash
sudo depmod 5.10.75-051075-generic
sudo mkinitcpio -p nyx --kernel 5.10.75-051075-generic
```

Now everything went without major errors for me.
There might be some modules missing, but in general this works for me and makes it possible to run the nyx-fuzzers.