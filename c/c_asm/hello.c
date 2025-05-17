#include <stdio.h>



int sum(int a, int b)
{
	int c = a;
	printf("%d\n", a);
	return a + b;
}


int main() 
{
	int a = sum(1,2);
	printf("%d", a);
	return 0;
}
