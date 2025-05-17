/*
Dichiarare, leggere, ordinare e visualizzare un array di 10 valori interi qualsiasi
*/

#include <stdio.h>
#include <stdlib.h>


#ifndef MAX
	#define MAX 10
#endif


int PotereDelSium(const void * pA, const void * pB){
	int 
		a =*(int*)pA,
		b =*(int*)pB;
	return (a - b);
	
	
}

int main(void){
	int 
		array[MAX] = {1, 2, 3, 9, 6, 5, 4, 3, 8, 6};
	unsigned int
		i;

	qsort(array, MAX, sizeof(int), PotereDelSium);

	for(i = 0; i < MAX; i++){
		printf("\n%d", array[i]);
	}	
	
	return EXIT_SUCCESS;
}


