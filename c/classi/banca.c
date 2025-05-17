#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/times.h>
#include <unistd.h>
#include "./banca.h"


// CLASSE CONTOBANCARIO
static inline struct ContoBancario*     contoBancario                (unsigned long long int, double);
static inline void                      ContoBancario__deposito      (struct ContoBancario*, double);
static inline double                    ContoBancario__prelievo      (struct ContoBancario*, double);
static inline void                      ContoBancario__trasferimento (struct ContoBancario*, struct ContoBancario*);
static inline void                      ContoBancario__str__         (struct ContoBancario*);
static inline void                      ContoBancario__del__         (struct ContoBancario*);

struct ContoBancario* contoBancario(const unsigned long long int num_conto, double saldo){

    struct ContoBancario *__init__ = (struct ContoBancario*) malloc (sizeof(struct ContoBancario));
    checker(__init__ == NULL, "errore nell'allocazione della memoria dinamicamente");

    __init__ -> numConto        = num_conto;
    __init__ -> saldo           = saldo;
    __init__ -> deposito        = ContoBancario__deposito;
    __init__ -> prelievo        = ContoBancario__prelievo;
    __init__ -> trasferimento   = ContoBancario__trasferimento;
    __init__ -> __str__         = ContoBancario__str__;
    __init__ -> __del__         = ContoBancario__del__;

    return __init__;
}


static inline void ContoBancario__deposito(struct ContoBancario* conto, double saldo){
    checker(saldo <= 0.0, "Impossibile depositare sul saldo un numero negativo");
    conto -> saldo += saldo;
    return;
}


static inline double ContoBancario__prelievo(struct ContoBancario* conto, double preleva){
    checker(preleva <= 0.0 || conto -> saldo - preleva <= 0.0, "Errore durante il prelievo");
    conto -> saldo -= preleva;
    return preleva;
}


static inline void ContoBancario__trasferimento(struct ContoBancario* conto1, struct ContoBancario* conto2){
    checker(conto1);
}


static inline void ContoBancario__str__(struct ContoBancario* conto){
    #ifndef CONTENT
        #define CONTENT conto -> saldo, conto -> numConto 
    #else
        #error, "CONTENT already defined"
    #endif
    printf("%f, %lld", CONTENT);
    #undef CONTENT
    return;
}


static inline void ContoBancario__del__(struct ContoBancario* conto){
    free(conto);
    return;
}
