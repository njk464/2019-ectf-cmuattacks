# Attacks
Their key weakness was that they left the ssh server with default credentials `root:root` - we exploit it for maximum damage!

`jailbreak`: Upload jailbreak program using SCP and run 

`ip`: Run the ip game, scp out the game into IDA and reverse to get the flag.

`hackermod`: Run the hackermod game, scp out the game and reverse the `flag_printout` function. Write a program that dumps the correct regions in memory and XORs them according to the flag_printout and run on the ArtyZ7. 

`pin_bypass`: Upload encrypted game to filesystem. Write the encrypted game to memory as expected by `mesh-game-loader`. Run mesh-game-loader. Enable +x permissions. Win.

`rollback`:Upload encrypted game to filesystem. Write the encrypted game to memory as expected by `mesh-game-loader`. Run mesh-game-loader. Enable +x permissions. Win

`pin_extraction`: Extract `/dev/mem` onto the SD card. Extract public key (which are null-terminated hex-strings), salt, nonce. Bruteforce corresponding PIN using `verifyPinFE` in `encryptPin.c`.
