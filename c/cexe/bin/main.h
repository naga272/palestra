#include <stdlib.h>
#include <string.h>
#include <errno.h>


#define opt3 __attribute__((optimize("O3")))

#ifndef len
    #define len(x) (sizeof(x) / sizeof(x[0]))
#else
    #error, "macro len already defined"
#endif


#ifndef checker
    #define checker(x)  \
        if (x) {\
            printf("errore %d: %s", errno, strerror(errno));\
            exit(errno);\
        }
#else
    #error, "macro checker already defined"
#endif


void io(void) opt3;
void for1(void) opt3;
void collatz(void) opt3;
void for2(void) opt3;
void rovesciaseq(void) opt3;
void dec_to_bin(void) opt3;
