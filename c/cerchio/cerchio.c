#include <stdio.h>
#include <math.h>

/*
	Dato in ingresso il raggio, calcolare la 
	lunghezza della circonferenza e l'area del cerchio.
*/

int main(void){
	float
		a, r, c;
	scanf("%d", &r);
	a = pow(r, 2) * 3.14;
	c = (r * 2) * 3.14;
	printf("area: %.3f\ncirconferenza: %.3f", a, c);
}
