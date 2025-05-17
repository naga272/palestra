#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "./domotica.h"


void logging(const char *filename, const char *percorso){
    /*
    *
    *   Funzione che ha il compito di loggare quando viene avviato il programma, da chi viene avviato, e che file viene avvitato
    *   L'output si trova in /log/trace.csv
    * 
    */
    FILE *f = fopen(percorso, "a");
    checker(f == NULL);


    time_t tempo = time(NULL);
    fprintf(f, "%ld;%s.c;%s\n", (long int) tempo, filename, ctime(&tempo));


    fclose(f);

    return;
}