
/*
 	Sto cercando di implementare a basso livello la classe chiamata Persona. 
	In python l'implementazione sarebbe:

	class Persona:
		def __init__(self, nome:str, cognome:str, eta:int):
			self.nome = nome
			self.cognome = cognome,
			self.eta = eta
		
		def incrementa_eta(self):
			self.eta += 1

		def __str__(self):
			return f"{self.nome}, {self.cognome}, {self.eta}"
*/


#ifndef checker 
	#define checker(x, msg) 					\
		if(x){							\
			printf("errore: %s", msg); exit(EXIT_FAILURE);	\
		}
#else
	#error, "macro checker already defined"
#endif

// prototype per istanziare gli oggetti
struct person* Persona(const char*, const char*, unsigned short int); // funzione che serve a generare una istanza della classe 


// classe persona
struct person{

	// proprieta classe
	char
		* nome,
		* cognome;

	unsigned short int 
		eta;

	// puntatore a funzione (metodi della classe)
	void			(*inc_eta)	(struct person*); 
	void 			(*__del__)	(struct person*);
	char*			(*__str__)	(struct person*);
};


// prototype dei metodi della classe Person
static inline void 	incrementa_eta(struct person*);
static inline void	object_delete(struct person*);	
static inline char* 	return__str__(struct person*);


struct person* Persona(const char* nome, const char* cognome, unsigned short int eta){

	struct person* __init__ 	= (struct person*) malloc(sizeof(struct person));
	checker(__init__ == NULL, "errore nell'allocare dinamicamente l'oggetto (problema struct)");

	__init__ -> nome 		= (char*) malloc(strlen(nome) - 1);
	__init__ -> cognome 		= (char*) malloc(strlen(cognome) - 1);

	checker(((__init__ -> nome == NULL) || (__init__ -> cognome == NULL)), "errore nell'allocare dinamicamente le proprieta dell'oggetto");


	/*	assegnazione valori alle proprieta'	*/
	strcpy(__init__ -> nome, nome);
	strcpy(__init__ -> cognome, cognome);
	__init__ -> eta 		= eta;

	/*		metodi della classe		*/
	__init__ -> inc_eta 		= incrementa_eta;
	__init__ -> __str__ 		= return__str__;	
	__init__ -> __del__		= object_delete;

	return __init__;
}


/*		
 *	METODI			
 *	I metodi non devono essere visibili esternamente,
 *	cioè bisogna prima istanziare l'oggetto per poter usare il metodo 
 *	della classe.
 *	Quindi, per renderle invisibili uso i token "static" e "inline".
 *	
 *	con il token "static" intendo dire che la funzione e' visibile solo 
 *	all'interno del file sorgente e quindi non accessbili da altri file.
 *
 *	con il token "inline" e' un ottimizzazione del compilatore, nel senso
 *	che durante la compilazione il codice della funzione viene inserito 
 *	direttamente all'interno del chiamante al posto di fare una chiamata
 *	di funzione. Serve in pratica a migliorare le prestazioni
 *	
 *	Molti esempi di funzioni dichiarate in questo modo si possono
 *	trovare all'interno del kernel di linux su GitHub. 
 *	Per esempio, all'interno del sorgente chiamato "cpu.c" esiste una funzione
 *	scritta in questo modo:  "static inline void cpuhp_lock_acquire(bool bringup)" (si trova a riga 102)
 *	Prendendo come esempio questa funzione e il suo contenuto, significa che questa funzione e'
 *	visibile solo all'interno di "cpu.c" e, che in fase di compilazione, viene inserito il codice
 *	della funzione cpuhp_lock_acquire all'interno della funzione chiamante, senza effettuare una call.
 *	Quindi, se dovessimo usare gdb per guardare il contenuto della funzione "cpuhp_thread_fun" (si trova a riga 1049)
 *	molto probabilmente non avremo: 
 *	
 *	push <valore_bool>
 *	call cpuhp_lock_acquire
 *
 *	ma bensì avremo direttamente il contenuto della funzione cpuhp_lock_acquire
 *	Questo e' come ho pensato che funziona "static inline"
 *
*/


static inline void incrementa_eta(struct person* oggetto){
	// funzione che incrementa l'eta della persona di 1
	oggetto->eta++;
}


static inline char* return__str__(struct person* oggetto){
	#ifndef BUFFER_SIZE
		#define BUFFER_SIZE 128
	#else
		free(oggetto);
		checker(1, "macro BUFFER_SIZE already defined");
	#endif

	static char stringa[BUFFER_SIZE];
	sprintf(stringa, "nome: %s cognome: %s eta: %d\n", oggetto->nome, oggetto->cognome, oggetto->eta);	

	return stringa;
}


static inline void object_delete(struct person* oggetto){
	free(oggetto);
}
