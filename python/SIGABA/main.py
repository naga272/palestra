import sys
import re
import os



"""
⚙️ Funzionamento passo-passo
STEP 0: Inizializzazione
Ogni gruppo di rotori ha una posizione iniziale (la chiave).

Ogni rotore è una permutazione non riflessiva (quindi non come Enigma).

STEP 1: Stepping
I 5 rotori di indicizzazione producono un output binario (diciamo 10 bit).

Quei bit vengono interpretati come un segnale su quali rotori di controllo devono ruotare.

I rotori di controllo generano a loro volta un altro pattern, che dice quali cifranti ruotano.

Quindi non è un sistema deterministico a rotazione fissa.
Ogni lettera ha un pattern di stepping potenzialmente diverso. È data-dependent e multi-layer.

STEP 2: Cifratura
Una volta aggiornate le posizioni, il carattere in ingresso attraversa i 5 cifranti in cascata, avanti (non c’è riflettore).

L’output è la lettera cifrata.
"""



class SIGABA():
    rotori = {
        "index" : {
            "S1": {
                "pos" : 0,
                "wiring" : [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 0, 25]
            },
            "S2": {
                "pos" : 0,
                "wiring" : [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25]
            },
            "S3": {
                "pos" : 0,
                "wiring" : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
            },
            "S4": {
                "pos" : 0,
                "wiring" : [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
            },
            "S5": {
                "pos" : 0,
                "wiring" : [5, 10, 15, 20, 25, 0, 4, 9, 14, 19, 24, 3, 8, 13, 18, 23, 2, 7, 12, 17, 22, 1, 6, 11, 16, 21]
            },    
        },
        "control" : {
            "K1": {
                "pos" : 0,
                "wiring" : [3, 1, 4, 0, 6, 2, 5, 9, 8, 7, 11, 13, 12, 14, 10, 15, 17, 16, 18, 19, 21, 20, 23, 22, 25, 24]
            },
            "K2": {
                "pos" : 0,
                "wiring": [6, 3, 0, 2, 1, 4, 5, 7, 8, 9, 10, 12, 11, 14, 13, 15, 16, 17, 18, 19, 20, 21, 23, 22, 25, 24]
            },
            "K3": {
                "pos" : 0,
                "wiring" : [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24]
            },
            "K4": {
                "pos" : 0,
                "wiring" : [25 - i for i in range(26)] # reverse alphabet
            },  
            "K5": {
                "pos" : 0,
                "wiring" : [i for i in range(26)]
            },      # identity (no mapping)
        },
        "chyper" : {
            "C1": {
                "pos" : 1,
                "wiring" : [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 9, 17, 2]
            },
            "C2": {
                "pos" : 2,
                "wiring" : [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 2, 16, 25, 7, 6, 15, 24, 12, 13, 5, 22, 4, 21, 19, 14]
            },
            "C3": {
                "pos" : 2,
                "wiring" : [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
            },
            "C4": {
                "pos" : 2,
                "wiring" : [5, 2, 25, 19, 0, 18, 23, 4, 22, 17, 3, 9, 6, 11, 15, 1, 13, 20, 24, 21, 8, 7, 16, 14, 10, 12]
            },
            "C5": {
                "pos" : 3,
                "wiring" : [20, 22, 24, 25, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
            },
        },
    }

    def __init__(self, char):
        self.char = char
        self.perm = self.permutazione()
        print(self.perm)

    def permutazione(self):
        i = (ord(self.char.upper()) - 65) % 26

        for key in SIGABA.rotori["cifranti"].keys():
            rotore = SIGABA.rotori["cifranti"][key]
            shift = (i + rotore["pos"] % 26)
            i = rotore["wiring"][shift]

        return i


    def __str__(self):
        return f'{self.char}'


def main():
    SIGABA("A")
    return 0


if __name__ == "__main__":
    result = main()
    print(f"uscita dal programma con valore {result}")
    sys.exit(result)
