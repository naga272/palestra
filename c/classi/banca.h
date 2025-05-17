#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/times.h>
#include <unistd.h>


unsigned short int      logging         (const char []);
extern void             _exit           (register int);

#ifndef checker
    #define checker(x, msg)                 \
        if(x){                              \
            printf("%s\n", msg);            \
            _exit(EXIT_FAILURE);            \
    }
#else
    #error, "macro checker already defined!"
#endif


// classe conto bancario
struct ContoBancario{
    // proprieta'
    unsigned long long int numConto;
    double saldo;

    // metodi
    void    (*deposito)         (struct ContoBancario*, double);
    double  (*prelievo)         (struct ContoBancario*, double);
    void    (*trasferimento)    (struct ContoBancario*, struct ContoBancario*);
    void    (*__str__)          (struct ContoBancario*);
    void    (*__del__)          (struct ContoBancario*);

};


// CLASSE CONTOCORRENTE

struct ContoCorrente{
    // eredita da ContoBancario
    struct ContoBancario *conto;

    // proprieta'
    double costoTransazione;
    unsigned short int freeTransazione;

    // metodi
    void    (*deposito)             (struct ContoCorrente*, double);
    double  (*prelievo)             (struct ContoCorrente*, double);
    void    (*deduzioneCommissione) (struct ContoCorrente*, struct ContoBancario*);
    void    (*__str__)              (struct ContoCorrente*);
    void    (*__del__)              (struct ContoCorrente*);

};
