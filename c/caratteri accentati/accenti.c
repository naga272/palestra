
#include <stdio.h>
#include <locale.h>


int main(void){
	setlocale(LC_ALL, "");
    printf(setlocale(LC_ALL,NULL));
    printf("\n�����\n");
    system("pause");
    return 0;
}
