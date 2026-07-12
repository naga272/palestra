from flask import Flask, session, request, render_template
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


@app.route("/")
def menu():
    return render_template("menu.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["nome"] = request.form["nome"]
        session["cognome"] = request.form["cognome"]
        session["mail"] = request.form["mail"]
        return render_template("menu.html", msg="LOGIN OK")
    return render_template("login.html")


@app.route("/mostra_sessione")
def mostra_sessione():
    if "nome" in session:
        dati = {
            "nome": session["nome"],
            "cognome": session["cognome"],
            "mail": session["mail"]
        }
        return render_template("sessione.html", dati=dati)
    return render_template("sessione.html", dati=None)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("menu.html", msg="LOGOUT OK")


# API per seconda applicazione
@app.route("/api/login", methods=["POST"])
def api_login():
    nome = request.form.get("nome")
    cognome = request.form.get("cognome")

    if nome and cognome:
        session["nome"] = nome
        session["cognome"] = cognome
        return "OK"
    return "KO"


@app.route("/api/utente")
def api_utente():
    if "nome" not in session:
        return "Autenticazione mancante"
    if session["nome"] and session["cognome"]:
        return "Utente presente"
    return "Utente non presente"


@app.route("/api/logout")
def api_logout():
    session.clear()
    return "Logout eseguito"


if __name__ == "__main__":
    app.run(port=5000)
