#include "./gc.h"


gc* myGc = NULL;


void __push(gc* self, void* ptr)
{
    checker(ptr == NULL, "errore! stai pushando nell'array di puntatori del garbage collecotr un ptr nullo")

    if (self->offset_ptr == self->len - 1) {
        self->len += 15;
        self->ptrs = realloc(self->ptrs, self->len * sizeof(void*));
        checker(ptr == NULL, "errore durante la reallocazione della memoria del garbage collector")
    }

    self->ptrs[self->offset_ptr] = ptr;
    self->offset_ptr++;

    /* debug per vedere lo stato effettivo dei ptr in self->ptrs
    
    for (size_t i = 0; i < self->offset_ptr + 1; i++) {
        printf("%p\n", self->ptrs[i]);
    }
    
    */
}


void __freeall(gc* self)
{
    for (size_t i = 0; i != self->offset_ptr; i++)
        if (self->ptrs[i] != NULL) // non si sa mai
            free(self->ptrs[i]);

    free(self->ptrs);
    free(self);
}


gc *DoGc() 
{
    gc *__init__ = (gc*) calloc((size_t) 15, sizeof(gc));
    checker(__init__ == NULL, "errore durante l'allocazione dinamica della memoria per il g.c.")
    
    // facciamo che appena inizia il programma, l'array dinamico ha una grandezza di 15 ptr
    // aggiorniamo di 15 alla volta, per evitare troppe chiamate a realloc durante la push dei nuovi ptr
    __init__->len           = 15; 
    __init__->ptrs          = calloc(__init__->len, sizeof(void*));
    __init__->offset_ptr    = 0;

    // metodi
    __init__->push      = __push;
    __init__->freeall   = __freeall;
    return __init__;
}


void init_gc()
{
    if (myGc == NULL)
        myGc = DoGc();
}


void free_gc()
{
    if (myGc != NULL)
        myGc->freeall(myGc);
}


void *gcmalloc(size_t bytes) 
{
    if (myGc == NULL) // se uno si dimentica di chiamare init_gc() a inizio programma, lo inizializzo qui
        myGc = DoGc();
    
    void *ptr = malloc(bytes);
    checker(ptr == NULL, "errore durante la chiamata a gcmalloc, malloc ha restituito NULL")

    myGc->push(myGc, ptr);
    return ptr;
}