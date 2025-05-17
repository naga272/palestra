#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include "./domotica.h"


/*
    *   
    *   CLASSE APPARTAMENTO
    *   Le firme delle funzioni static inline devono rimanere all'interno di questo modulo, insieme al loro corpo, 
    *   perchè altrimenti verrà dato errore.
    *   Per static ci si riferisce a una funzione visibile SOLO a questo modulo, per inline si usa per 
    *   una ottimizzazione del codice. In pratica, il compilatore quando incontra una chiamata a una funzione
    *   static inline sposta tutto il contenuto di questa al posto della chiamata, evitando così ogni volta
    *   il settaggio dello stack.
    *   vedi moduli del kernel fatti da torvalds: 
    *       - https://github.com/torvalds/linux/blob/master/kernel/cpu.c)
    * 
*/
static inline void      __add(struct Appartamento*, struct Elettrodomestico*);
static inline void      __remove(struct Appartamento*, struct Elettrodomestico*);
static inline double    __potenza(struct Appartamento*);
static inline void      __accendiTutti(struct Appartamento*);
static inline void      __spegniTutti(struct Appartamento*);
static inline char*     __str(struct Appartamento*);
static inline void      __del(struct Appartamento*);


struct Appartamento* appartamento(void){
    struct Appartamento*__init__ = (struct Appartamento*) calloc(1, sizeof(struct Appartamento));
    checker(__init__ == NULL);

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
    // ogni oggetto ha __str__() che ritorna un vettore di 100 char, quindi faccio 100 * numero oggetti in appartamento
    static char stringa[100 * 50];
    stringa[0] = '\0'; 

    unsigned int i = 0;
    while(i < 50){
        if(app -> vettore[i] != NULL){
            char temp[51];
            sprintf(temp, "%s\n", app -> vettore[i] -> __str__(app -> vettore[i]));
            strcat(stringa, temp);
        }
        i++;
    }
    return stringa;
}


static inline void __del(struct Appartamento* app){
    for(unsigned short int i = 0; i < 50; i++)
        if(app -> vettore[i] != NULL)
            app -> vettore[i] -> __del__(app -> vettore[i]);

    free(app);
}


/*
    *
    *   CLASSE ELETTRODOMESTICO
    *
*/
static unsigned int id = 0;
static inline double     potenza__  (struct Elettrodomestico*);
static inline char*      str__      (struct Elettrodomestico*);
static inline void       del__      (struct Elettrodomestico*);


struct Elettrodomestico* elettro(char nome[], short unsigned int status, double potenzaWatt){
    struct Elettrodomestico* __init__ = (struct Elettrodomestico*) malloc(sizeof(struct Elettrodomestico));
    checker(__init__ == NULL);

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
    static char stringa[100];
    sprintf(stringa, "id oggetto: %i, stato: %i, nome: %s, potenza Watt: %.2f", e ->id, e->status, e->nome, e->potenzaWatt);
	return stringa;
}


static inline void       del__      (struct Elettrodomestico* e){
    free(e);
    return;
}
