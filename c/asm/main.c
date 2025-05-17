#include <stdio.h>
#include <stdlib.h>
#include <string.h>


extern void _exit(register int);
int main(void);


void _start(){
	int result = main();
	_exit(result);
}


int main() {
    	int a = 10, b = 12, c = 2, d = 5;
	int result;

	__asm__ (
        	"PUSH {r4, lr}\n"
        	"MOV r4, %[a]\n"
        	"ADD r4, r4, %[b]\n"
        	"ADD r4, r4, %[c]\n"
        	"ADD %[result], r4, %[d]\n"
        	"POP {r4, pc}"
        	: [result] "=r" (result)
        	: [a] "r" (a), [b] "r" (b), [c] "r" (c), [d] "r" (d)
        	: "r4"
    	);

	printf("%d\n", result);
	return EXIT_SUCCESS;
}