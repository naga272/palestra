#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	int 
		lunghezza;
	char
		parola[20],
		despacito = "hola\0";
	
	printf("parola: ");
	scanf("%s",&parola);
	if(strcmp(parola, despacito)== 0){
		printf("parole uguali");
	}
	else{
		printf("parole diverse");
	}
}
