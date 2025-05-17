/*
PROBLEMA 1
Scrivere un programma Python che chiesti in input nome, cognome e classe di 
uno studente, mostri sullo schermo un messaggio di benvenuto personalizzato. 
Per esempio dati ‘Piero’, ‘Rossi’, ‘3AA’ il programma potrebbe mostrare la frase:
“Benvenuto Piero Rossi nella mitica 3AA!’

BASTIANELLO FEDERICO
29/09/2022
*/

#include <stdio.h>				//LIBRERIA STANDARD INPUT/OUTPUT
#include <string.h>				//LIBRERIA PER LE VARIABII TYPE STRINGHE
#include <stdlib.h>				//LIBRERIA STANDARD 

int main(){						//PROCEDURA PRINCIPALE
	
	//VARIABILI LOCALI
	char nome[20];		//variabile di tipo stringa, il max di caratteri è 20 (si rappresenta tra quadre dopo il nome)
	char cognome[20];	
	char classe[10];
	
	printf("nome: ");
	scanf("%s",&nome);
	printf("cognome: ");
	scanf("%s",&cognome);
	printf("classe: ");
	scanf("%s",&classe);
	printf("Benvenuto %s", nome);
	printf(" %s", cognome);
	printf(" nella mitica ");
	printf("%s\n", classe);
	
	system("pause");	
}
