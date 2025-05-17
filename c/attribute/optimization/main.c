#include <stdio.h>
#include <stdlib.h>


int sum(int, int) __attribute__((optimize("O3"), warning("This is a warning message")));


int hidden_variable __attribute__((visibility("hidden")));

int main(){
	hidden_variable = 3;
	printf("%d\n", sum(12, 23));
	printf("%d\n", hidden_variable);
	return EXIT_SUCCESS;
}


int sum(int a, int b){return a + b;}
