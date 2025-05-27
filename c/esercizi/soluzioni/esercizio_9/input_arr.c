#include <stdio.h>


int main(){

	int array[4] = { 3, 4, 5, 6 };

	printf("numero: ");
	scanf("%d", &array[2]);
	printf("\nIn nuovo valore che abbiamo inserito: %d\n", array[2]);
}
