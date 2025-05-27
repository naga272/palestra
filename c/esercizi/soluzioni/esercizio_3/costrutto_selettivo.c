#include <stdio.h>
#include <stdint.h>


int main(){
	uint8_t number;
	printf("inserire numero: ");
	scanf("%hhi", &number);

	if(number <= 10 && number >= 0)
		printf("il valore che hai inserito e': %hhi", number);
	else
		printf("Invalid number\n");
	return 0;
}
