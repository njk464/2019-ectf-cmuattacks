#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 0
fi

DIR=../$1
tmp_gdb=./temp_gdb_commands

echo "target remote localhost:1234" > $tmp_gdb
echo "add-symbol-file $DIR/u-boot.elf" >> $tmp_gdb

arm-linux-gnueabihf-gdb -x $tmp_gdb

rm $tmp_gdb
