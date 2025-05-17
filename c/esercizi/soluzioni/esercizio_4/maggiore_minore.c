#include <stdio.h>


int main(){
	int a, b;

	printf("Inserisci valore per il primo numero: ");
	scanf("%d", &a);
	
	printf("\nInserisci valore per il secondo numero: ");
	scanf("%d", &b);

	printf("il numero più grande inserito e': %d\n", (a > b)? a : b);
}

