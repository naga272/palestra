#include <stdio.h>

/*
  Valore e indirizzo sono diversi.
*/



int main() {
  int a=60;
  int *p;

  p=&a;		

  printf("&a=%x a=%x\n", &a, a);
  printf("&p=%x p=%x\n", &p, p);

  return 0;
}