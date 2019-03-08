#!/bin/bash

set -e 

if [ "$#" -ne 1 ] && [ "$#" -ne 2 ] && [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
fi

DIR=../$1
shift

FLAGS=""

if [ ! -f $DIR/u-boot.elf ]; then
  echo "Cannot find the u-boot kernel"; exit 1;
elif [ ! -f $DIR/system.dtb ]; then
  echo "Cannot find the system device tree"; exit 1;
elif [ ! -f $DIR/image.ub ]; then 
  echo "Cannot find the system kernel"; exit 1;
elif [ ! -f ./sdcard.img ]; then
  echo "Cannot find the sdcard image"; exit 1;
fi

serial_dev=stdio

if [ "$1" == "serial" ]; then
    serial_dev=pty
    shift
fi

if [ "$2" == "serial" ]; then
    serial_dev=pty
    2=$1
    shift
fi

if [ "$1" == "gdb" ]; then
  FLAGS="${FLAGS} -s -S"
  shift
fi

source /opt/pkg/petalinux/settings.sh

qemu-system-aarch64 -M arm-generic-fdt-7series -machine linux=on -serial $serial_dev -display none -kernel $DIR/u-boot.elf -dtb $DIR/system.dtb -drive file=./sdcard.img,if=sd,format=raw -device loader,file=$DIR/image.ub,addr=0x10000000 ${FLAGS}
