#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <locale.h>
#include <errno.h>


#ifndef checker
    #define checker(x) if(x){           \
        printf(strerror(errno), errno); \
        exit(EXIT_FAILURE);             \
    }
#else
    #error, "macro checker already defined"
#endif


// gli ambienti linux e quelli windows creano cartelle in modo diverso, 
// quindi hanno header separati
#if __unix__
    #include <sys/stat.h>
    void do__linux__(const char*);
#else
    #include <direct.h>
    // _mkdir(const char *pathname);
    void do__windows__(const char*);
#endif


void create_readme(const char*);
void create_changelog(const char*);
void create_pythonfile(const char*);