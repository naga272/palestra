#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <locale.h>
#include <errno.h>
#include "./header.h"


int main(int argc, char *argv[]){

    checker(argc != 2)

    #if __unix__
        // mkdir(const char *pathname, mode_t mode)
        do__linux__(argv[1]);
    #endif

    #if WIN32 || WIN64
        do__windows__(argv[1]);
    #endif


    return EXIT_SUCCESS;
}