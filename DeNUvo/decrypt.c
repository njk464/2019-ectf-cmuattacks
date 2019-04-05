#include "prince_ref.h"
#include <stdio.h>

void rev(uint8_t arr[8]) {
    for (size_t i = 0; i < 4; i++) {
        uint8_t f = arr[i];
        arr[i] = arr[7 - i];
        arr[7 - i] = f;
    }
}

int main(){
    uint8_t in_bytes[8];
    uint8_t key_bytes[16] = {0x54, 0x7b, 0xb2, 0x83, 0x30, 0x02, 0xf1, 0x8c, 0x9f, 0x69, 0x6e, 0xa3, 0x64, 0xd5, 0x30, 0xcd};
    uint8_t out_bytes[8];
    
    FILE *f;
    f = fopen("kernel.enc","rb");
    FILE *o;
    o = fopen("out.out", "wb");
    fseek(f, 0, SEEK_END);
    int fileSize = ftell(f);
    fseek(f, 0, SEEK_SET);
    printf("File Size: %d\n",  fileSize);
    int numRead;
    for(int i = 0; i < fileSize-8; i = i + 8){
        numRead = fread(in_bytes, 1, 8, f);
        if (numRead < 1){
            printf("Error reading\n");
            break;
        }
        if (numRead < 8){
            printf("End? %s\n", in_bytes);
        }
        rev(in_bytes);
        prince_decrypt(in_bytes, key_bytes, out_bytes);
        rev(out_bytes);
        // printf("%s", out_bytes);
        fwrite(out_bytes, 1, 8, o);
    }
    fclose(f);
}