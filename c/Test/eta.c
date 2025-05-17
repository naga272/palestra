/*
    L’utente inserisce la propria età e il
    programma dice se è maggiorenne (ovvero
    con età maggiore uguale a 18 anni)
*/

#include <stdio.h>
#include <stdlib.h>
#include <locale.h>

int main(void){
    int
        eta;
    printf("inserire eta: ");
    scanf("%d", &eta);
    (eta >= 18)? printf("e maggiorenne") :  printf("e minorenne");
    return 0;
}
