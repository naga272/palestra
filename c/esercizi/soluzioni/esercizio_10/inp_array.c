#include <stdio.h>


int main(){
	int array[4];

	for(size_t i = 0; i < 4; i++){
		printf("\nInserire numero:");
		scanf("%d", &array[i]);	
	}

	for(size_t i = 0; i < 4; i++)
		printf("%d\n", array[i]);


	return 0;
}
