# Emulating zynq 7000 SoC board in qemu
Follow the instructions to create qemu machine emulator for loading u-boot/mesh and linux kernel.

Note: Run `petalinuxenv` in the shell before running `qemu` or `petalinux-config`. Ensure petalinux environment is set for every new shell session.

## Copying files from MES to here
  * To copy the important files from MES into the attacks repository please run `./copy_files.sh TEAM_DIR`. This will copy the necessary files for qemu into a new directory (../TEAM_DIR)

## Known Issues
  * When the linux kernel is loaded, an i2c driver sends a timout message to dmesg (stdout) every 5 seconds. This message is printed out on the serial console which makes it hard to type shell commands, since the error messages fill up the screen. 

## Setting SDCARD Image file
  * Run the shell script `./create-sd.sh TEAM_DIR` to create an sdcard raw image file - `sdcard.img`. The script will copy the games from `../TEAM_DIR/games` folder. 

## Launch Qemu
  * Ensure u-boot, linux kernel and the device tree is built using provisionSystem.py. Check if the following files exists:
    * `../TEAM_DIR/u-boot.elf`
    * `../TEAM_DIR/image.ub`
    * `../TEAM_DIR/system.dtb`
  * Start qemu by running the `./start-qemu.sh TEAM_DIR`. 

## Petalinux config (in case of spi error)
  * Checking out this branch should inherit the changes to petalinux config. If QEMU/U-BOOT THOWS AN SPI ERROR ON THE SCREEN, follow the below steps and rebuild the kernel and dtb (run the provisionSystem.py again).
    1. cd /home/vagrant/MES/Arty-Z7-10
    2. petalinux-config -c u-boot
    3. select: Device Drivers -> SPI flash support -> STMICRO SPI flash support (press y to select) 
    4. save and exit

# Run GDB with QEMU 
Before starting, make sure to set the petalinux environment variables using `petalinuxenv`. Run qemu by passing the `gdb` as the second or third argument. 

```bash
~/MES/qemu> ./start-qemu.sh TEAM_DIR gdb
```
Launch `./run_gdb TEAM_DIR` in a separate terminal window and make sure that you have run `petalinuxenv`

# Run QEMU with a Serial device
Before starting, make sure to set the petalinux environment variables using `petalinuxenv`. Run qemu by passing the `serial` as the second or third argument. 

```bash
~/2019-ectf-cmuattacks/qemu> ./start-qemu.sh TEAM_DIR serial
```
This will cause the qemu session to read and write from `/dev/pts/3`. Which can be accessed in pythonlike this

```python
ser = serial.Serial("/dev/pts/3")
```

*** 

[source](https://draskodraskovic.wordpress.com/2012/05/27/debugging-u-boot-in-qemu-2/)

