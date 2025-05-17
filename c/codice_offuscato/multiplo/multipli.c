#include <stdio.h>
#include <stdlib.h>

/*

	Il programma legge due numeri e controlla se il primo è multiplo del secondo.

*/

#ifndef DIH
	#define DIH main
	#define DES int
	#define DIH_ void
	#define DAH {
	#define DAH_ }
	#define _DAH ;
	#define __DIH__ scanf
	#define DEH (
	#define DEH_ )
	#define DID printf
#endif


DES DIH DEH DIH_ DEH_ DAH

	DES
		a = 0,
		i = 0,
		b = 0 _DAH		
	
	//richiesta numeri

	DID DEH "inserisci primo numero: " DEH_ _DAH
	__DIH__ DEH "%d", &a DEH_ _DAH	
	
	DID DEH "inserisci secondo numero: " DEH_ _DAH
	__DIH__ DEH "%d", &b DEH_ _DAH


	(a % b == 0)?DID DEH "e multiplo" DEH_ : DID DEH "non e multiplo" DEH_ _DAH
	
	
	return EXIT_SUCCESS _DAH
DAH_



