#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./domotica.h"


//metodi classe appartamento
// add, remove, potenza, accendiTutti, spegniTutti, str, del
static inline void      __add(struct Appartamento*, struct Elettrodomestico*)       __attribute__((optimize("03")));
static inline void      __remove(struct Appartamento*, struct Elettrodomestico*)    __attribute__((optimize("03")));
static inline double    __potenza(struct Appartamento*)                             __attribute__((optimize("03")));
static inline void      __accendiTutti(struct Appartamento*)                        __attribute__((optimize("03")));
static inline void      __spegniTutti(struct Appartamento*)                         __attribute__((optimize("03")));
static inline char*     __str(struct Appartamento*)                                 __attribute__((optimize("03")));
static inline void      __del(struct Appartamento*)                                 __attribute__((optimize("03")));


struct Appartamento* appartamento(void){
    struct Appartamento*__init__ = (struct Appartamento*) malloc(sizeof(struct Appartamento));
    checker(__init__ == NULL, "ERRORE durante la creazione dell'istanza di appartamento");

    __init__ -> add          = __add;
    __init__ -> remove       = __remove;
    __init__ -> potenza      = __potenza;
    __init__ -> accendiTutti = __accendiTutti;
    __init__ -> spegniTutti  = __spegniTutti;
    __init__ -> __str__      = __str;
    __init__ -> __del__      = __del;

    return __init__;
}


// funzioni per CLASSE appartemento
static inline void __add(struct Appartamento* app, struct Elettrodomestico* e){
    app -> vettore[e -> id] = e;
}


static inline void __remove(struct Appartamento* app, struct Elettrodomestico* e){
    free(app -> vettore[e -> id]);
}


static inline double __potenza(struct Appartamento* app){
    double totWatt = 0;
    for(unsigned int i = 0; i < 50; i++)
        (app -> vettore[i] -> status = True)? totWatt += app -> vettore[i] -> potenzaWatt : 0;

    return totWatt;
}


static inline void __accendiTutti(struct Appartamento* app){
    for(unsigned int i = 0; i < 50; i++)
        app -> vettore[i] -> status = True;
}


static inline void __spegniTutti(struct Appartamento* app){
    for(unsigned int i = 0; i < 50; i++)
        app -> vettore[i] -> status = False;
}


static inline char* __str(struct Appartamento* app){
    static char stringa[400]; // Assicurati che stringa abbia abbastanza spazio
    stringa[0] = '\0'; // Assicurati che la stringa sia inizializzata come una stringa vuota

    for(unsigned short int i = 0; i < 50; i++) {
        if(app->vettore[i] != NULL) {
            char temp[200]; // Stringa temporanea per memorizzare la rappresentazione dell'elettrodomestico corrente
            sprintf(temp, "%s\n", app->vettore[i]->__str__(app->vettore[i])); // Formatta la rappresentazione elettrodomestico corrente
            strcat(stringa, temp); // Concatena la rappresentazione corrente a stringa
        }
    }
    return stringa;
}

static inline void __del(struct Appartamento* app){
    for(unsigned short int i = 0; i < 50; i++)
        if(app -> vettore[i] != NULL)
            app -> vettore[i] -> __del__(app -> vettore[i]);

    free(app);
}


// funzioni per CLASSE Elettrodomestico
static unsigned int id = 0;
static inline double     potenza__  (struct Elettrodomestico*) __attribute__((optimize("03")));
static inline char*      str__      (struct Elettrodomestico*) __attribute__((optimize("03")));
static inline void       del__      (struct Elettrodomestico*) __attribute__((optimize("03")));


struct Elettrodomestico* elettro(char nome[], short unsigned int status, double potenzaWatt){
    struct Elettrodomestico* __init__ = (struct Elettrodomestico*) malloc(sizeof(struct Elettrodomestico));
    checker(__init__ == NULL, "ERRORE durante la creazione dell'istanza di Elettrodomestico");
    
    __init__ -> id = id;
    strcpy(__init__ -> nome, nome);
    __init__ -> status = status;
    __init__ -> potenzaWatt = potenzaWatt;
    __init__ -> potenza = potenza__;
    __init__ -> __str__ = str__;
    __init__ -> __del__ = del__;

    id++;    
    return __init__;
}


static inline double     potenza__  (struct Elettrodomestico* e){
    return e -> potenzaWatt;
}


static inline char*      str__      (struct Elettrodomestico* e){
    static char stringa[200];
    sprintf(stringa, "id oggetto: %i, stato: %i, nome: %s, potenza Watt: %.2f", e ->id, e->status, e->nome, e->potenzaWatt);
	return stringa;
}


static inline void       del__      (struct Elettrodomestico* e){
    free(e);
    return;
}
