#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

/*
* Unico file .c che contiene tutti gli esercizi. Basta settare la chiamata di funzione nel main()
*/

#define opt3 __attribute__((optimize("O3")))

#ifndef len
    #define len(x) (sizeof(x) / sizeof(x[0]))
#else
    #error, "macro len already defined"
#endif


#ifndef checker
    #define checker(x)  \
        if (x) {\
            printf("errore %d: %s\n", errno, strerror(errno));\
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


void io(void)
{
    FILE
        *inp = fopen("./flussi/input.txt", "r"),
        *out = fopen("./flussi/output.txt", "w");
    
    int n;

    checker(inp == NULL || out == NULL);
    fscanf(inp, "%d", &n);
    fprintf(out, "%d", n);

    fclose(inp);
    fclose(out);
    return;
}


void for1()
{
    FILE
        *inp = fopen("./flussi/input.txt", "r"),
        *out = fopen("./flussi/output.txt", "w");
    
    unsigned int N;

    checker(inp == NULL || out == NULL);
    fscanf(inp, "%ui", &N);

    for (unsigned int i = 1; i != N + 1; i++) {
        fprintf(out, "%u ", i);
    }

    fclose(inp);
    fclose(out);
    return;
}


/*
*   da qui in poi non uso più file, tanto è sempre la identica storia, 
*   li scrivo direttamente a schermo per comodità di scrittura
*/
void collatz()
{
    int N, count_while = 1;
    scanf("%i", &N);
    
    while (N != 1) {
    
        if (N % 2 == 0) {
            N = N / 2;
        } else if (N % 2 == 1) {
            N = N * 3 + 1;
        }
        printf("%i\n", N);
        count_while++;
    }
    printf("numero di cicli: %i", count_while);
    return;
}


void for2()
{
    int N;
    scanf("%i", &N);
    for (unsigned int i = 1; i <= N; i++) {
        for (unsigned int z = 1; z <= N; z++) {
            printf("%i ", z * i);
        }
        printf("\n");
    }
    return;
}


void rovesciaseq()
{
    int array[] = {1, 2, 3, 4, 5, 6, 7, 8};
    for (size_t i = len(array) - 1; i != -1; i--)
        printf("%i ", array[i]); 

    return;
}


void dec_to_bin()
{
    int N = 34;
    size_t i = 0; // lo uso come indice array
    short int array[64];

    if (N == 0) {
        printf("0\n");
        return;
    }
    
    while (N > 0) {
        array[i++] = N % 2;
        N = N / 2;
    }

    // Stampa i bit in ordine corretto
    for (int j = i - 1; j >= 0; j--)
        printf("%d", array[j]);

    printf("\n");
    return ;
}


int main()
{
    io();
    return EXIT_SUCCESS;
}
