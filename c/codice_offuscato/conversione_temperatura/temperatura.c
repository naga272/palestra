
#include <stdio.h>
#include <stdlib.h>

/*

3) L’utente inserisce una temperatura in Celsius e il calcolatore la 
converte in Fahrenheit ed in Kelvin. Se la temperatura 
inserita è minore dello zero assoluto (-273,15), il calcolatore segnala un errore.
Si ricordi che:
Fahrenheit = (9/5) · Celsius + 32
Kelvin = Celsius + 273,15

*/

#ifndef DIH
	#define DIH main
	#define DES int
	#define DIH_ void
	#define DAH {
	#define DAH_ }
	#define ___DAH char
	#define _DAH ;
	#define __DIH__ scanf
	#define DEH (
	#define DEH_ )
	#define DID printf(
	#define DUD float
#endif


DES DIH DEH DIH_ DEH_ DAH 
	___DAH
		des[] = "inserire temperatura in Celsius: " _DAH
	
	DUD 
		a, b _DAH
	
	// richiesta temperatura in celsius
	DID "%s", des DEH_ _DAH
	__DIH__ DEH "%f", &a DEH_ _DAH	

	//conversione in Fahrenheit = (9/5) · Celsius + 32
	b = ((9 / 5) * a) + 32 _DAH
	DID "\nconversione in Fahrenheit: %.3f", b DEH_ _DAH
	//conversione in Kelvin = Celsius + 273,15
	b = a + 273,15 _DAH
	DID "\nconversione in Fahrenheit: %.3f", b DEH_ _DAH

	return EXIT_SUCCESS _DAH

DAH_

