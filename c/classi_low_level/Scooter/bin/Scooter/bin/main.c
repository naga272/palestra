#include <stdio.h>
#include <stdlib.h>
#include <locale.h>

#include "scooter.h"


int main(int argc, char *argv[], char *envp[]){
	setlocale(LC_CTYPE, " ");

	struct scooter *p1 = Scooter(12.0, 13.0, 15, 18); // creo un'istanza

	p1 -> capacita = 18.0;

	printf("capacità: %.2f\n", p1->capacita);

	p1 -> __del__(p1);		// libero la memoria allocata dinamicamente
	return EXIT_SUCCESS;
}

