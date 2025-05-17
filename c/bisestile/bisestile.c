#include <stdio.h>

/*
	L’utente inserisce un anno ed il calcolatore 
	verifica se l’anno inserito è bisestile.
	Un anno è bisestile se è divisibile per 4 ma non per 100, 
	oppure se è divisibile per 400 (ad esempio il 1900 non è stato bisestile, 
	mentre il 2000 lo è stato).
*/

int main(void){
	int a;
	
	printf("inserire anno: ");
	scanf("%d", &a);
	(a % 4 == 0 && a % 100 != 0 && a % 400 == 0)?printf("bisestile") : printf("non bisestile");	
	return 0;
}
