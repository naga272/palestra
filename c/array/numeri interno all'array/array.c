#include <stdio.h>
#include <stdlib.h>

#define NumElementi(array) (sizeof(array)/sizeof(array[0]))	//calcolo il numero di elementi all'interno dell'array

void main(void) {
	int 
		Numeri[] = {2, 4, 6, 8, 9, 2, 12, 56, 78, 21},
        i,
        max = NumElementi(Numeri);
    
	printf("Numero di elementi dell'array: %d", max);	//stampo il numero di elementi 	
	for(i = 0; i < max; i++){
		printf("\n%d", Numeri[i]);
	}
	printf("\n");
	system("pause");
	
}
