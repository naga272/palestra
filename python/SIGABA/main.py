import sys


"""
Funzionamento passo-passo
STEP 0: Inizializzazione
Ogni gruppo di rotori ha una posizione iniziale (la chiave).

Ogni rotore è una permutazione non riflessiva (quindi non come Enigma).

STEP 1: Stepping
I 5 rotori di indicizzazione producono un output binario (diciamo 10 bit).

Quei bit vengono interpretati come un segnale su quali rotori
di controllo devono ruotare.

I rotori di controllo generano a loro volta un altro pattern,
che dice quali cifranti ruotano.

Quindi non è un sistema deterministico a rotazione fissa.
Ogni lettera ha un pattern di stepping potenzialmente diverso.
E' data-dependent e multi-layer.

STEP 2: Cifratura
Una volta aggiornate le posizioni,
il carattere in ingresso attraversa i 5 cifranti in cascata,
avanti (non c'e' riflettore).

L'output è la lettera cifrata.
"""


class SIGABA():
    rotori = {
        "index": {
            "S1": {
                "pos": 0,
                "wiring": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
            },
            "S2": {
                "pos": 0,
                "wiring": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
            },
            "S3": {
                "pos": 0,
                "wiring": [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
            },
            "S4": {
                "pos": 0,
                "wiring": [14, 25, 24, 23, 22, 21, 20, 19, 18, 17]
            },
            "S5": {
                "pos": 0,
                "wiring": [5, 10, 15, 20, 25, 0, 4, 9, 14, 19]
            },
        },
        "control": {
            "K1": {
                "pos": 0,
                "wiring": [3, 1, 4, 0, 6, 2, 5, 9, 8, 7, 11, 13, 12, 14, 10, 15, 17, 16, 18, 19, 21, 20, 23, 22, 25, 24]
            },
            "K2": {
                "pos": 0,
                "wiring": [6, 3, 0, 2, 1, 4, 5, 7, 8, 9, 10, 12, 11, 14, 13, 15, 16, 17, 18, 19, 20, 21, 23, 22, 25, 24]
            },
            "K3": {
                "pos": 0,
                "wiring": [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16, 19, 18, 21, 20, 23, 22, 25, 24]
            },
            "K4": {
                "pos": 0,
                "wiring": [25 - i for i in range(26)]  # reverse alphabet
            },
            "K5": {
                "pos": 0,
                "wiring": [i for i in range(26)]
            },      # identity (no mapping)
        },
        "chyper": {
            "C1": {
                "pos": 1,
                "wiring": [
                    4, 10, 12, 5, 11, 6, 3, 16, 21, 25,
                    13, 19, 14, 22, 24, 7, 23, 20, 18,
                    15, 0, 8, 1, 9, 17, 2
                ]
            },
            "C2": {
                "pos": 2,
                "wiring": [
                    0, 9, 3, 10, 18, 8, 17, 20, 23, 1,
                    11, 2, 16, 25, 7, 6, 15, 24, 12,
                    13, 5, 22, 4, 21, 19, 14
                ]
            },
            "C3": {
                "pos": 2,
                "wiring": [
                    1, 3, 5, 7, 9, 11, 2, 15, 17, 19,
                    23, 21, 25, 13, 24, 4, 8, 22, 6,
                    0, 10, 12, 20, 18, 16, 14
                ]
            },
            "C4": {
                "pos": 2,
                "wiring": [
                    5, 2, 25, 19, 0, 18, 23, 4, 22, 17,
                    3, 9, 6, 11, 15, 1, 13, 20, 24, 21,
                    8, 7, 16, 14, 10, 12
                ]
            },
            "C5": {
                "pos": 3,
                "wiring": [
                    20, 22, 24, 25, 0, 2, 4, 6, 8, 10,
                    12, 14, 16, 18, 1, 3, 5, 7, 9, 11,
                    13, 15, 17, 19, 21, 23
                ]
            },
        },
    }

    def __init__(self, char):
        self.char = char
        self.rotori_index = SIGABA.rotori["index"]

    def encrypt(self) -> str:
        # tutti i rotori index girano di 1 x ogni char premuto

        print("\n---- Index Rotor ----")
        # for rotore in self.rotori_index:
        #    print(self.rotori_index[rotore])

        num_from_index = self.logic_index(self.rotori_index)
        print("\n")

        # for rotore in self.rotori_index:
        #    print(self.rotori_index[rotore])

        print("\n\n\n---- Control Rotor ----")

        self.logic_control(num_from_index)

    def logic_control(self, num_from_index: list):
        flags_control_rotor = []

        # si attiva k1 se la somma dei numeri della lista col modulo di
        # 10 e' maggiore di 5
        k1 = True if sum(num_from_index) % 10 > 5 else False
        flags_control_rotor.append(k1)

        # si attiva se la somma dei numeri della lista e' pari
        k2 = True if sum(num_from_index) % 2 == 0 else False
        flags_control_rotor.append(k2)

        # si attiva k3 se tra i numeri di num_from_index c'è un 10
        k3 = True if 10 in num_from_index else False
        flags_control_rotor.append(k3)

        k4 = True if all(num < 10 for num in num_from_index) else False
        flags_control_rotor.append(k4)

        # si attiva solo se almeno 3 segnali sono > 5
        k5 = True if sum(num > 5 for num in num_from_index) > 3 else False
        flags_control_rotor.append(k5)

        print(flags_control_rotor)

    def logic_index(self, rotori_index: dict) -> list:
        signals = []
        step = 1

        for rotore in self.rotori_index:
            self.rotori_index[rotore]["pos"] = (self.rotori_index[rotore]["pos"] + step) % len(self.rotori_index[rotore]["wiring"])

            # prendo il carattere della lista che si trova a posizione pos
            wiring = self.rotori_index[rotore]["wiring"]
            position = self.rotori_index[rotore]["pos"]
            signals.append(wiring[position])

        return signals

    def gira_rotore(self, rotore: dict, steps: int) -> dict:

        rotore["pos"] = (rotore["pos"] + steps) % len(rotore["wiring"])

        for i in range(steps):
            first_chr = rotore["wiring"][0]

            for x in range(0, len(rotore["wiring"]) - 1, 1):
                chr_right = rotore["wiring"][x + 1]
                rotore["wiring"][x] = chr_right

            rotore["wiring"][len(rotore["wiring"])-1] = first_chr

        return rotore

    def __str__(self):
        return f"{self.char}"


def main():
    SIGABA("A").encrypt()
    return 0


if __name__ == "__main__":
    result = main()
    print(f"uscita dal programma con valore {result}")
    sys.exit(result)
