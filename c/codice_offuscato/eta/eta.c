/*

L’utente inserisce la propria età e il programma dice 
se è maggiorenne (ovvero con età maggiore uguale a 18 anni)

*/


#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef DIH
	#define DUH__ 40
	#define DIH main
	#define DES unsigned int
	#define DIH_ void
	#define DAH {
	#define DAH_ }
	#define _DAH ;
	#define __DAH__ char 
	#define __DIH__ scanf
	#define DEH (
	#define DEH_ )
	#define DID printf
	#define DUH struct
#endif



DUH _DUH DAH 
	__DAH__ ds[DUH__] _DAH
	DES i _DAH
DAH_ _DAH


DES DIH(DIH_)DAH 
	
	DUH _DUH _DUH_ _DAH //struct _DUH _DUH_ ;	

	strcpy(_DUH_.ds, "inserire eta: ") _DAH	

	DID DEH "%s", _DUH_.ds DEH_ _DAH
	__DIH__ DEH "%d", & _DUH_.i DEH_ _DAH	
	if DEH _DUH_.i >= 18 DEH_ DAH 
		DID DEH "e maggiorenne" DEH_ _DAH
	DAH_  else DAH 
		DID DEH "e minorenne" DEH_ _DAH
	DAH_
	
	return EXIT_SUCCESS _DAH
DAH_




