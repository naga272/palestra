#include <stdio.h>   // contiene la firma della funzione printf()
#include <stdint.h>  // contiene il tipo int16_t


/*
    *
    * Consegna: 
    *   Creare programma variabili.c che:
    *       - dichiara una variabili di tipo intero e gli venga assegnato il valore 125
    *       - dichiara una variabile di tipo int16_t assegna come valore 128
    *       - stampa a schermo la somma delle due variabili
    * 
    * Compilazione:
    *   - Windows: gcc ./variabili.c -o ./variabili.exe
    *   - Linux:   gcc ./variabili.c -o ./variabili
    *
    * Author:
    *   - Bastianello Federico
    *
*/


int main(){
    int a = 125;
    int16_t b = 128;    // dichiaro una variabile di tipo intero a 16 bit e gli assegno il valore 128

    printf("La somma di a + b e': %i", a + b); 
    // %i viene sostituito dal risultato dell'operazione di a + b. 
    //Questo perche' e' una stringa formattata

    return 0;
}
