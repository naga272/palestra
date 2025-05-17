#include <stdio.h>

/* 
    L’utente inserisce una temperatura in Celsius e il 
    calcolatore la converte in Fahrenheit ed in Kelvin. 
    Se la temperatura inserita è minore dello zero assoluto (-273,15), 
    il calcolatore segnala un errore.
    Si ricordi che:
    Fahrenheit = (9/5) · Celsius + 32
    Kelvin = Celsius + 273,15
*/

int main(void){
    float Celsius, Kelvin, Fahrenheit;
    printf("temperatura in Celsius: ");
    scanf("%d", &Celsius);
    Fahrenheit = ((9 / 5) * Celsius) + 32;
    Kelvin = Celsius + 273,15;
    printf("\nFahrenheit: %d\nKelvin:%d", Fahrenheit, Kelvin);
}

