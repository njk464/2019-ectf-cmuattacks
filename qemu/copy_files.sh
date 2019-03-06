#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 0
fi

DIR=../$1

if [ ! -d "$DIR" ]; then
    mkdir $DIR
fi

echo "copying u-boot.elf"
cp /home/vagrant/MES/Arty-Z7-10/images/linux/u-boot.elf $DIR/.
echo "copying image.ub"
cp /home/vagrant/MES/Arty-Z7-10/images/linux/image.ub $DIR/.
echo "copying system.dtb"
cp /home/vagrant/MES/Arty-Z7-10/images/linux/system.dtb $DIR/.
echo "copying FactorySecrets.txt"
cp /home/vagrant/MES/tools/files/generated/FactorySecrets.txt $DIR/.
echo "copying games"
cp -r /home/vagrant/MES/tools/files/generated/games $DIR/. 
