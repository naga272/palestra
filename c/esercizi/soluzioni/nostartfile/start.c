#include <stdio.h>

/*
    *
    *   Di default, qualunque programma quando viene compilato, in automatico gli
    *   viene aggiunto la procedura _start(), che è esattamente da dove il programma comincia.
    *   In questo esempio vi mostro che e' possibile personalizzare l'entry point   
    *   come si vuole.
    *
    *   In pratica, il compilatore modifica il codice in questo modo (ho fatto una semplificazione):
    *   section .text
    *       Global _start
    *   
    *   _start: call main
    *           mov rdi, rax    ; rdi contiene lo stato di uscita dalla funzione main
    *   _exit:  mov rax, 60     ; uscita dal programma con valore rax
    *           syscall
    *
    *   main:   push rbp
    *           mov rbp, rsp
    *           ; ... codice funzione main ...
    *           leave       ; libero lo stack
    *           mov rax, 0  ; ritorno il valore della funzione main nel registro rax
    *           ret
    *
    *   NB: in caso vogliate compilare questo programma assembly dovete usare il compilatore nasm e il linker ld
    *       $nasm -f elf64 -g ./start.asm -o ./start.o
    *       $ld ./start.o -o ./start
    *
    * - compilazione:
    *   Il programma può essere compilato solo su os Linux-like, Per windows e' un po diverso
    *   $gcc -Wall -W -Wextra -nostartfiles ./start.c -o ./start
    *
    *   e' molto importante aggiungere il flag -nostartfiles, questo perchè serve a far capire al compilatore
    *   che non deve creare lui la procudera _start
    *
    * - author:
    *   Bastianello Federico
    *
*/


/* firme delle funzioni */
extern void _exit(register int);
int main(void);


void _start(){
    printf("Hello from _start() function");
    // posso chiamare la funzione main tutte le volte che voglio
    main();
    int result = main();
    _exit(result);  // uscita dal programma
}


int main(){
    printf("Hello from main() function\n");
    return 0;
}
