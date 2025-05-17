#include <stdio.h>

int main(){
	unsigned int n;

	printf("Inserisci numero: ");
	scanf("%d", &n);

	for(unsigned int i = 0; i < n; i ++)
		if(i % 2 == 0)
			printf("%d\n", i);


	return 0;
}
