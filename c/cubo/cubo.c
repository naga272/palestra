#include <stdio.h>
#include <math.h>

/*
Scrivere i seguenti programmi in linguaggio C (controllare che l'input immesso dall'utente sia corretto):
1. Dato in ingresso un numero N visualizzare in output il suo cubo.
2. Dato in ingresso il raggio, calcolare la lunghezza della circonferenza e l'area del cerchio.
3. Dato un tempo espresso in ore, minuti e secondi, calcolare il corrispondente valore in secondi e visualizzarlo.
4. Dato un tempo in secondi, calcolare a quante ore, minuti e secondi corrisponde, visualizzando l'output.
*/

int main(void){
	int n;
	scanf("%d", &n);
	n = pow(n, 3);
	printf("%d", n);
	return 0;
}
