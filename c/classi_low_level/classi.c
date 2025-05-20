#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <string.h>

#include "persona.h"


int main(int argc, char *argv[], char *envp[]){
	setlocale(LC_CTYPE, " ");

	// ritorna una istanza della struct con valori gia assegnati
	struct person *prova = Persona("Mario", "rossi", 19);
	printf("\n%s", prova -> __str__(prova));

	prova -> inc_eta(prova);
	printf("\n%s", prova -> __str__(prova));

	//printf("\n%s", __str__(prova));

	prova -> __del__(prova);
	return EXIT_SUCCESS;
}

