#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
	int a = 11;
	int x = 0;
	int y = 1;
	
	while (x != y){
		printf("%d\n", a);
		a = a + 11;
	}
	system("/npause");
}
