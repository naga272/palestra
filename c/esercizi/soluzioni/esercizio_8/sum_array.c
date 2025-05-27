#include <stdio.h>


int main(){

	int 
		n = 0,
		array[10] = {
			12, 
			34, 
			544, 
			1, 
			23, 
			9, 
			6, 
			787, 
			67, 
			10
		};

	/*
	 *	
	 *	Il tipo size_t equivale a dire 'unsigned int'.
	 *	Dato che la lunghezza degli array e' sempre maggiore
	 *	di 0, non ha senso avere un indice che usa il bit
	 *	più significativo per rappresentare i numeri negativi
	 *
	*/

	for(size_t i = 0; i < 10; i++)
		n += array[i];

	printf("somma di tutti gli elementi: %d\n", n);
	return 0;
}
