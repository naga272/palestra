#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/times.h>
#include <locale.h>
#include "./domotica/domotica.h"



int main(int argc, char *argv[], char *envp[]){
    setlocale(LC_CTYPE, " ");

    struct Appartamento*     app = appartamento();

    struct Elettrodomestico* forno = elettro("forno", True, 1.0);
    struct Elettrodomestico* aspirapolvere = elettro("aspirapolvere", True, 1.0);
    struct Elettrodomestico* frigorifero = elettro("frigorifero", False, 1.0);

    app -> add(app, forno);
    app -> add(app, aspirapolvere);
    app -> add(app, frigorifero);

    printf("%s\n", app -> __str__(app));

    app -> __del__(app);
    return EXIT_SUCCESS;
}