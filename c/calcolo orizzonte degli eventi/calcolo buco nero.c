/*calcolo dell'orizzonte degli eventi e accelerazione gravitazione di un buco nero e di un'altra massa*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

int main()
{
	//DICHIARAZIONE VARIABILI LOCALI
	float g = 0.00000000000667; 			//costante gravitazione universale
	int m_buco_nero;						//masse solari del buco nero
	float m_solare;							//massa del sole
	int x;									//valore booleano
	int i;									//valore booleano
	float r;								//raggio orizzonte degli eventi
	int velocita;							//velocita della luce
	
	velocita = 299792458;
	x = 0;
	i = 1;
	
	printf("\nstampa costante %.14f\n", g);
	
	while (x != i) {
		printf("\nmassa buco nero espressa in massa solare: ");
		scanf("%d", &m_buco_nero);
		m_solare = ((1.989 * (pow(10, 30))) * m_buco_nero);
		printf("\n\nla massa in kg del buco nero e': '%0.f", m_solare);
		r = (((2 * g * m_solare) / (pow(velocita, 2))) / 100);
		printf("\nil raggio dell'orizzonte degli eventi e': %.10f", r);
		printf("\n\nvuoi far ripartire il programma? \nse si premi 0, altrimenti premi 1: ");
		scanf("%d", &x);	
	}
		
	printf("\nfine programma\n");
	printf("\n");
	system("pause");
}
