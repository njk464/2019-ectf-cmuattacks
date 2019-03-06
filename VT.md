
# Potential attacks
- No integrity check on game body
- Extra large games
  - Appending bytes (i.e. 512M of 'A') to a predefined game leads to r2/r0 control when we play the game

```
U-Boot 2017.01 (Mar 04 2019 - 23:58:40 +0000)

Model: Zynq Arty Z7 Development Board
Board: Xilinx Zynq
I2C:   ready
DRAM:  ECC disabled 508 MiB
MMC:   sdhci@e0100000: 0 (SD)
SF: Detected s25fl128s_64k with page size 256 Bytes, erase size 64 KiB, total 16 MiB
*** Warning - bad CRC, using default environment

In:    serial@e0000000
Out:   serial@e0000000
Err:   serial@e0000000
Model: Zynq Arty Z7 Development Board
Board: Xilinx Zynq
Net:   No ethernet found.
SF: Detected s25fl128s_64k with page size 256 Bytes, erase size 64 KiB, total 16 MiB
Enter your username:
Enter your username: demo
Enter your PIN: 00000000
mesh> list
ipflag-v1.0
hackermod-v1.0
mesh> play ipflag-v1.0
data abort
pc : [<1e71a5c0>]          lr : [<1fb8c94c>]
reloc pc : [<02bdf5c0>]    lr : [<0405194c>]
sp : 1e71a620  ip : 00000000     fp : 00000000
r10: 00000000  r9 : 1e71aee8     r8 : 00000000
r7 : 00000000  r6 : 00000000     r5 : 00000000  r4 : 00000000
r3 : e0100000  r2 : ffffffff     r1 : 00000000  r0 : 00000000
Flags: nZCv  IRQs off  FIQs off  Mode SVC_32
Resetting CPU ...

resetting ...
[eCTF] Booting team vtech


U-Boot 2017.01 (Mar 04 2019 - 23:58:40 +0000)

Model: Zynq Arty Z7 Development Board
Board: Xilinx Zynq
I2C:   ready
DRAM:  ECC disabled 508 MiB
MMC:   sdhci@e0100000: 0 (SD)
SF: Detected s25fl128s_64k with page size 256 Bytes, erase size 64 KiB, total 16 MiB
*** Warning - bad CRC, using default environment

In:    serial@e0000000
Out:   serial@e0000000
Err:   serial@e0000000
Model: Zynq Arty Z7 Development Board
Board: Xilinx Zynq
Net:   No ethernet found.
SF: Detected s25fl128s_64k with page size 256 Bytes, erase size 64 KiB, total 16 MiB
Enter your username: demo
Enter your PIN: 00000000
mesh> list
ipflag-v1.0
hackermod-v1.0
mesh> play ipflag-v1.0
data abort
pc : [<1fb62784>]          lr : [<1fb8c94c>]
reloc pc : [<04027784>]    lr : [<0405194c>]
sp : 1e71a5f8  ip : 00000000     fp : 00084530
r10: 000cdf09  r9 : 1e71aee8     r8 : 00000030
r7 : 0000f8dc  r6 : 1e71a624     r5 : 00000020  r4 : 1e71b8f0
r3 : 00000028  r2 : 41414141     r1 : 000cdf09  r0 : 41414141
Flags: nZCv  IRQs off  FIQs off  Mode SVC_32
Resetting CPU ...
```

# Attacks that don't work
- Ethernet based attacks
- Bruteforcing 
