#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>
#include "./domotica/domotica.h"


extern void logging(const char*, const char*);


int main(int argc, char *argv[], char *envp[]){
    setlocale(LC_CTYPE, " ");
    logging(argv[0], "./log/trace.csv");

    struct Appartamento*     app            = appartamento();
    struct Elettrodomestico* forno          = elettro("forno", True, 1.0);
    struct Elettrodomestico* aspirapolvere  = elettro("aspirapolvere", True, 1.0);
    struct Elettrodomestico* frigorifero    = elettro("frigorifero", False, 1.0);

    app -> add(app, forno);
    app -> add(app, aspirapolvere);
    app -> add(app, frigorifero);

    printf("%s\n", forno -> __str__(forno));
    printf("%s\n", aspirapolvere -> __str__(aspirapolvere));
    printf("%s\n\n", frigorifero -> __str__(frigorifero));

    printf("%s", app -> __str__(app));


    app -> __del__(app);
    return EXIT_SUCCESS;
}