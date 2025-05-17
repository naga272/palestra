#include <stdio.h>
#include <stdlib.h>


/*
	se il preprocesso MAX non e definito lo creo 
*/

#ifndef MAX 
	#define MAX 10 
#endif

/*
1) Dichiarare un array di 10 elementi interi che contiene il numero di alunni per classe 
(>15 e <33) visualizza la media degli alunni per classe.
Attenzione nome array n_alunni
in un ciclo leggere l'array
in un ciclo calcolare la somma degli alunni che servirà al calcolo della media
nome file array1.c



2) Dichiarare un array di 10 voti e calcolare la media dei voti, trovare il voto più alto
nome array voti
in un ciclo leggere l'array
in un ciclo calcolare la somma per calcolare la media
in un ciclo trovare il voto più alto
*/

unsigned int
	voti[MAX] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
	n_alunni[MAX] = {16, 17, 18, 19, 20, 25, 32, 22, 24, 30}, // array di 10 elementi
	i,
	funzione1(unsigned int *n_alunni),
	funzione2(unsigned int *voti);


int main(void){
	unsigned int
		a,
		b;

	a = funzione1(n_alunni) / MAX;
	printf("\nla media di alunni per classe e': %u", a);
	b = funzione2(voti) / MAX;
	printf("\nla media voti: %u", b);
	return EXIT_SUCCESS;
}


unsigned int funzione1(unsigned int *n_alunni){
	//funzione che somma il numero di studenti delle classi
	unsigned int
		c = 0;

	for(i = 0; i < MAX; i++){
		c += n_alunni[i];
		printf("\n%u", c);
		
	}
	return c;
}


unsigned int funzione2(unsigned int *voti){
	// funzione che calcola la somma dei voti e stampa a schermo il voto maggiore
	unsigned int 
		c = 0, 
		d = 0;

	for(i = 0; i < MAX; i++){
		c += voti[i];
		if(d < voti[i])
			d = voti[i];
	}
	printf("\nil voto maggiore e: %u", d);
	return c;
}
