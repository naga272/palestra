#include <stdio.h>


int main(){
	unsigned int n;

	printf("Inserisci numero positivo:");
	scanf("%d", &n);

	for(unsigned int i = 0; i < n; i++)
		printf("%d\n", i);
}
