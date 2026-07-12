import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import sys


def tasso_totale(tasso_interesse, tasso_rischio, inflazione):
    return 1 + (tasso_interesse + tasso_rischio + inflazione) / 100


def ROE(patrimonio_netto, pred_futuro_corr):
    return (pred_futuro_corr / patrimonio_netto) * 100


def trend(x: list, y: list) -> LinearRegression:
    '''
    weellll, per fortuna qualcun'altro ha pensato di fare la regressione lineare
    prima di me (erano c*zzi a causa del tempo concesso), non ho tempo per imparare la
    regressione lineare, quindi uso la classe preassemblata LinearRegression
    '''
    known_x = np.array(x).reshape(-1, 1)
    known_y = np.array(y)

    model = LinearRegression(fit_intercept=True)
    model.fit(known_x, known_y)

    new_x = np.linspace(1, 5, 100).reshape(-1, 1)
    pred = model.predict(new_x)

    plt.scatter(known_x, known_y, label='Dati noti')
    plt.plot(new_x, pred, color='red', label='Trend')
    plt.legend()
    plt.xlabel('Anno')
    plt.ylabel('y')
    plt.title('trend()')

    plt.xticks(
        known_x.flatten(),
        [f"Anno {int(x)}" for x in known_x.flatten()]
    )

    plt.show()

    print("Coefficiente angolare:", model.coef_[0])
    print("Intercetta:", model.intercept_)
    return model


def main():
    anni_passati = [1, 2, 3, 4, 5]
    utile_netto = [50000, 300000, 280000, 390000, 520000]

    model = trend(
        anni_passati,
        utile_netto
    )

    anni_futuri = np.array([6, 7, 8, 9, 10]).reshape(-1, 1)
    pred_futuro = model.predict(anni_futuri)

    tasso_interesse = 3.41
    tasso_rischio = 5.5
    inflazione = 0.6

    pred_futuro_corr = pred_futuro * tasso_totale(tasso_interesse, tasso_rischio, inflazione)

    # per il calcolo del ROE bisogna avere il patrimonio netto
    # senza di quello non posso far nulla
    patrimonio_netto = 20000

    roe = ROE(patrimonio_netto, pred_futuro_corr)

    plt.plot(anni_passati, utile_netto, 'bo-', label="Dati storici")
    plt.plot(anni_futuri, pred_futuro_corr, 'ro--', label="proiezione con tasso")
    plt.xlabel('anno')
    plt.ylabel('utile netto previsto (€)')
    plt.title('proiezione redditività futura e ROE stimato')
    plt.legend()
    plt.show()

    print("\nProiezione utile netto (corretta con tassi):")
    for anno, utile, r in zip(range(6, 11), pred_futuro_corr, roe):
        print(f"Anno {anno}: Utile previsto = {utile:,.2f} €, ROE = {r:.2f}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
