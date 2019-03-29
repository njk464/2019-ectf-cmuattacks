#!/usr/bin/env python3.6

import os
import subprocess
import argparse

# the directory to mount the sd card to
BOOT_MNT = '/mnt/zynq/boot/'
GAMES_MNT = '/mnt/zynq/games'

# the names to copy the boot and mes files to on the sd card
BOOT_FILE = 'BOOT.bin'
MES_FILE = 'MES.bin'


def copy_file(src, dst):
    """
    This function copies a files from the src path to the destination path.
    This is used for copying files to the sd card.

    src: a path to the source file to copy.
    dst: a path to the destination file to copy.
    """

    if not os.path.isfile(src):
        raise IOError("File does not exist: %s" % (src))

    subprocess.check_call("sudo cp %s %s" % (src, dst), shell=True)


def setup_sdcard(device):
    """
    This function sets up the sd card by formatting it with the correct
    partitions and the correct filesystems. It uses the sfdisk format file
    which can be found in the ectf_sd.fdisk file in this directory.

    device: the path to the device to be formatted, ie /dev/sdb. This must be
            the overall device, not a partition on the device.
    """

    print("Formatting SD Card...")
    # format sd card and create filesystems
    subprocess.check_call(f"sudo sfdisk --force {device} < ectf_sd.sfdisk > /dev/null", shell=True)
    subprocess.check_call(f"sudo mkfs.fat -F 32 -n BOOT -I {device}1 > /dev/null", shell=True)
    subprocess.check_call(f"sudo mkfs.ext2 -L games {device}2 > /dev/null", shell=True)
    subprocess.check_call(f"sudo tune2fs -e panic {device}2 >/dev/null", shell=True)
    # put install data in the last partition
    subprocess.check_call(f"sudo dd if={storage of={device}3 bs=1M > /dev/null", shell=True)

    print("Done Formatting SD Card")
    print("    BOOT : %s1" % (device))
    print("    games : %s2" % (device))
    print("    data : %s3 " % (device))


def copy_games(device, games):
    """
    This function copies all the games from the specified games directory
    to the device specified. The device is the overall device and it copy the
    games to the second partition (the games partition).

    device: the path to the device to copy the games to, ie /dev/sdb.
    games: the path to the directory that contains the games to copy to the
            sd card. This script will copy ALL regular files in the root of
            the specified directory, so make sure it is a clean directory.
    """

    print("Copying Games...")
    # mount sd card
    subprocess.check_call("sudo mkdir -p %s" % (GAMES_MNT), shell=True)
    subprocess.check_call("sudo mount %s2 %s" % (device, GAMES_MNT), shell=True)

    # copy each game specified in games file
    src_files = os.listdir(games)
    for file_name in src_files:
        full_path = os.path.join(games, file_name)
        try:
            print("    %s-> %s2/" % (full_path, device))
            copy_file(full_path, GAMES_MNT)
        except IOError as e:
            print(e)
            subprocess.check_call("sudo umount %s" % (GAMES_MNT), shell=True)
            exit(1)

    # cleanup
    subprocess.check_call("sudo umount %s" % (GAMES_MNT), shell=True)

    print("Done Copying games to SD Card")


def copy_boot(device, boot_path, mes_path=None):
    """
    This function copies the boot file from the specified file paths
    to the device specified. The device is the overall device and it will copy
    the specified files to the first partition (the boot partition).

    device: the path to the device to copy the games to, ie /dev/sdb.
    boot_path: The path to the boot file to use. This will always copy
            the file with the name BOOT_FILE specified above.
    mes_path: An optional path to a secondary boot image. This will
            always be name MES.bin. This is used when copying both an
            image with the authenticated fsbl and an image with uboot and the
            kernel on it.
    """

    print("Copying Images to SD Card...")

    # mount sd card
    subprocess.check_call("sudo mkdir -p %s" % (BOOT_MNT), shell=True)
    subprocess.check_call("sudo mount %s1 %s" % (device, BOOT_MNT), shell=True)

    # copy boot binary
    try:
        if mes_path:
            print("    %s-> %s" % (mes_path, os.path.join(device + "1", MES_FILE)))
            copy_file(mes_path, os.path.join(BOOT_MNT, MES_FILE))
        print("    %s-> %s" % (boot_path, os.path.join(device + "1", BOOT_FILE)))
        copy_file(boot_path, os.path.join(BOOT_MNT, BOOT_FILE))
    except IOError as e:
        print(e)
        subprocess.check_call("sudo umount %s" % (BOOT_MNT), shell=True)
        exit(1)

    # cleanup
    subprocess.check_call("sudo umount %s" % (BOOT_MNT), shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('device',
                        help=("This is the SD device to deploy the "
                              "system on to."))
    parser.add_argument('boot_path',
                        help=("This is the path to the main file to boot the "
                              "system. This could be either MES.bin "
                              "(for an unauthenticated fsbl) or BOOT.bin "
                              "(for an authenticated fsbl)"))
    parser.add_argument('mes_path',
                        help=("This is the path to MES.bin generated by "
                              "packageSystem.py. This is required if using the "
                              "authenticated fsbl"),
                        nargs='?')
    parser.add_argument('games',
                        help=("This is the directory where provision games "
                              "are stored. This process deploys them to the "
                              "correct location."))
    parser.add_argument('--noformat',
                        action="store_true",
                        help=("This is an optional argument. "
                              "If it is specified, then the SD card will not "
                              "be formatted. Caution, if the sd card is "
                              "not already formatted correctly, this "
                              "script will fail."))
    args = parser.parse_args()

    # verify boot bin
    boot_file = args.boot_path
    if not os.path.isfile(boot_file):
        print("Unable to open %s. You must copy the provided BOOT.bin to "
              "that location in order to run this script" % (boot_file))
        exit(2)

    # verify device
    if not os.path.exists(args.device):
        print("Error, SD device does not exist: %s" % (args.device))
        exit(2)
    # verify games folder
    if not os.path.isdir(args.games):
        print("Error, games directory doesn't exist: %s" % (args.games))
        exit(2)

    # unmount sd card just in case
    subprocess.call("sudo umount %s* &> /dev/null" % (args.device), shell=True)

    # build images and provision sd card
    if not args.noformat:
        setup_sdcard(args.device)

    copy_boot(args.device, boot_file, mes_path=args.mes_path)
    copy_games(args.device, args.games)

    exit(0)


if __name__ == '__main__':
    main()
