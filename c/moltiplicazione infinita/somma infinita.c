/**/

#include <stdio.h>
#include <stdlib.h>

int main(){
	int a, b, c;
	
	a = 0;
	b = 1;
	c = 0;
	
	while(a != b){
		c = c + 1;
		printf("\nnumero: %d", c);
	}
	system("pause");
}
