# 2019-ectf-cmuattacks
Repository for keeping track of our attack scripts during the Embedded CTF

## Requirements

Before running any of the scripts in this repository please run the following commands
```
sudo apt install python-pip3
pip3 install -r requirements.txt
```

## Brute Force Logins script

Needs to be run with sudo priveleges so `/dev/ttyUSB1` can be accessed.

# Possible Attacks

There are several key goals that we want to achieve in the attacks:

1) `hackermod`: Win an unwinnable game
2) `ip`: Read a plaintext string from the decrypted game
3) `jailbreak`: Get arbitrary code execution in petalinux to read `mesh_drm`
4) `pin_bypass`: Access a user/run games from a user you don't have the PIN for
5) `pin_extraction`: Get the pin of a user you don't have the PIN for
6) `rollback`: Run an older version of a game already installed

This can be achieved in the following ways
- Arbitrary memory read in mesh shell -> this gives us access to the decrypted mesh shell so we can read the secrets!
- Code execution in mesh shell -> same as above, or we can even run games as other users!
- Code execution/shell for Petalinux -> read the game, run any arbitrary game, win any game!
- Unauthenticated writing to flash -> allows us to overwrite metadata can rollback games
- Weaknesses in cryptography (detailed below)


## Easy Attacks
There's a bunch of easy attacks we should try first before delving deep into the source code/documentation

- Run `strings` on all the games that are provided -> for the `ip` flag
- Check whether ssh/telnet is disabled on `192.168.1.3` when the game is loaded -> `ip` flag, `jailbreak` flag
- Whether debug commands like `dump` and `resetflash` are present
- Buffer overflow in username/pin fields -> most flags
- Just directly check if rollback works -> `rollback` flag

## Medium Attacks
By this point, we should look into the source and look into the basic underlying crypto to see if they protect against the basic attack vectors

- Bruteforce pin - for `pin_extraction` and `pin_bypass`
- Hard-coded secret keys/credentials
- Ways to escape to shell in `startup.sh`
- Lack of encryption in flash memory for user metadata - reflash to get `rollback` flag
- Check if games are signed - `hackermod` 
- Check if `ext4load` was used without the size flag - that means we can just inject any arbitrary large file and achieve overflow!

## Hard Attacks
Now we have to dive deep into the binaries and exact working of the crypto to see if we can use anything. This includes

- Reuse of nonces
- Signing doesn't sign the whole binary - we manipulate the encrypted binary somehow!
- Other weaknesses in cryptography - hash extension attacks, etc.
- Vulnerabilities in the games
- Vulnerabilities in their mesh shell
