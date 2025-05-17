#include <stdio.h>

/*
    Il programma legge due numeri e controlla
    se il primo è multiplo del secondo.
*/

int main(void){
    int a = 0;
    int b = 0;
    printf("primo numero: ");
    scanf("%d", &a);
    printf("\nsecondo numero: ");
    scanf("%d", &b);
    (b % a == 0)? printf("b multiplo di a") : printf("b non multiplo di a");
    return 0;
}
