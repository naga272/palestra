#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#ifndef len_array // calcolo la lunghezza di un qualcunque tipo di array
    #define len_array(x) (sizeof(x) / sizeof(x[0]))
#else
    #error, "macro len_array already defined"
#endif


void *my_memcmp(void *data, int c, size_t n){
    /*
    *
    *   Argv:
    *       - data: puntatore all'array, viene modificato dopo il tipo
    *       - c: valore che riceverà ogni elemento dell'array
    *       - n: grandezza array
    * 
    */
    int *mem = (int*) data; 
    /*
    *
    *   *mem e *data puntano allo stesso blocco di memoria, di conseguenza
    *   se provo a cambiare gli elementi di uno, cambiano anche con l'altro
    * 
    */

    for(size_t i = 0; i < n; i++)
        mem[i] = c;

    return data; // ritorno il ptr
}


int main(void){
    // Viene inizializzato un vettore di interi, poi stampa il suo contenuto
    int x[5] = {1, 2, 3, 4, 5};
    for(size_t i = 0; i < len_array(x) ; i++)
        printf("%d\n", x[i]);


    // cambio il valore di tutti i parametri dell'array a 0, non ha bisogno di un 
    // assegnazione perchè ritorna il ptr di tipo void
    my_memcmp(x, 0, sizeof x); 


    //stampo a schermo il nuovo array
    for(size_t i = 0; i < sizeof(x) / sizeof(int); i++)
        printf("%d\n", x[i]);

    return EXIT_SUCCESS;
}