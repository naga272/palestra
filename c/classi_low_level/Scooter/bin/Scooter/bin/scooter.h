#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*
 *
 *	nome: 		Federico Bastianello
 *	classe: 	4AA
 *	data: 		24 / 02 / 2024
 *	
 *	consegna: 	1) Implementare in C la classe Scooter, inserendo i controlli nel costruttore e fornendo uno
 *			o piu metodi per trasformare un oggetto in una stringa. Commentare opportunamente il codice.
 *			
 *			filosofia della struttura sulla classe Scooter:
 *			- Uno scooter possiede un serbatoio con una certa capacita (in litri), una certa quantita	
 *			  di carburante nel serbatoio, una determinata resa del carburante (misurata in km/l cioe'
 *			  chilometri / litro) ed un contachilometri per registrare i kmPercorsi.
 *			
 *			- il metodo rifornimeto() serve per aggiungere carburante nel serbatoio
 *			
 *			- il metodo avanza() data la distanza da percorrere, riduce la quantita di carburante nel
 *			  serbatoio a seconda della resa e aggiorna il valore del contachilometri
 *			
 *			- il metodo reset_km() azzera il contachilometri
 *			
 *			- la classe e' in grado di tenere traccia di quanti scooter sono stati creati.
 *			
 *			- Ciascun scooter nasce con un codice id. univoco
 *			
 *			- le variabili di istanza devono essere protette, in particolare capacita e resa sono visibili
 *			  ma non modificabili; mentre quantita di carburante e km percorsi sono visibile e possono
 *			  essere modificati solo tramite l'uso dei metodi avanza(), rifornimento() e reset().
 *			
 *			- Il numero di scooter non deve essere modificabile, ma solo leggibile
 *			
 *			- lo stesso vale per codice identificante di ciascun scooter  
 * 
*/


#ifndef checker
	extern void _exit(register int);	// corrisponde a:
						// _exit: mov rax, 60
						// 	  mov rdi, 1 ; 1 corrisponde a EXIT_FAILURE per comunicare l'uscita con successo si usa 0
						// 	  syscall

	#define checker(x, msg)			\
		if(x){				\
			printf("%s\n", msg); 	\
			_exit(1);		\
		}
#else
	#error, "macro checker already defined"
#endif


#ifndef buffer_x_all
	// provo a ricreare anche la proprieta di classe chiamata all[] di python, che colleziona tutti gli oggetti creati, es:
	// class Scooter():
	// 	all = []
	// 	def __init__(self, x):
	// 		self.x = x
	// 		Scooter.all.append(self)
	//
	// non c'entra con l'esercizio, la voglio solo supporre un'implementazione della all[]
	// sarebbe un vettore di struct scooter
	// se dealloco una struct da main si dovrebbe liberare lo spazio precedentemente occupato dalla struct nel vettore all
	#define buffer_x_all 5000
#else
	#error, "MACRO buffer_x_all already defined"
#endif


struct scooter{
	//proprieta classe
	unsigned int
		id;
	float 
		capacita, 
		quantita,
		resa,
		contachilometri;
	
	// puntatori alle funzioni della classe
	const void 	(*rifornimento) (struct scooter*, float);
	const void	(*avanza) 	(struct scooter*, float);
	const void	(*reset)	(struct scooter*);

	const void 	(*__del__) 	(struct scooter*);
	const char* 	(*__str__) 	(struct scooter*);
};

// prototype della funzione usata per istanziare gli oggetti
struct scooter*		Scooter		(const float, float, float, float);

