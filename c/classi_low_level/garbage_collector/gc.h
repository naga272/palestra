#ifndef GC_H
#define GC_H


#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define checker(x, msg)         \
    if (x) {                    \
        printf("%s\n", msg);    \
        exit(EXIT_FAILURE);     \
    }


typedef struct garbage_collector {
    void **ptrs;
    void (*push) (struct garbage_collector*, void*);
    void (*freeall) (struct garbage_collector*);
    size_t len;         // len massima dell'array di ptr
    size_t offset_ptr;  // quanti ptr inseriti effettivamente nell'array
} gc;

extern gc *DoGc();
extern void init_gc();
extern void __push(gc* self, void* ptr);
extern void __freeall(gc* self);
extern void *gcmalloc(size_t bytes);
extern void free_gc();

#endif