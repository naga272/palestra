#include <stdio.h>
#include <stdlib.h>

#define NumElement(array) (sizeof(array)/sizeof(array[0]))
void main(void){
	int 
		array[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
	
	for(int i = 0; i < NumElement(array); i++){
		printf("%d", array[i]);
	}
	
}
