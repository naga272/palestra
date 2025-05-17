#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <locale.h>
#include <sys/types.h>
#include <sys/times.h>
#include <unistd.h>
#include "./banca.h"


unsigned short int logging(const char nome_programma[]){    
    FILE *logg = fopen("./log/trace.csv", "a");
    checker(logg == NULL, "errore nell'apertura del file");

    time_t time_now;

    fprintf(logg, "username: %s, operative system %s, timestamp: %ld, nome programma: %s\n", 
                getenv("USERNAME"), (__unix__)? "Linux" : "Windows", time(&time_now), nome_programma);

    fclose(logg);

    return EXIT_SUCCESS;
}


int main(int argc, char *argv[], char *envp[]){
    setlocale(LC_CTYPE, " ");
    checker(logging("banca") == EXIT_FAILURE, "errore nella creazione del file log!");

    return EXIT_SUCCESS;
}
