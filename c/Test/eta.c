/*
    L�utente inserisce la propria et� e il
    programma dice se � maggiorenne (ovvero
    con et� maggiore uguale a 18 anni)
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
