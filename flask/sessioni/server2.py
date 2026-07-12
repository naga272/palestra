import requests

url = "http://127.0.0.1:5000"

session = requests.Session()

# LOGIN
data = {
    "nome": "Mario",
    "cognome": "Rossi"
}

r = session.post(url + "/api/login", data=data)
print("LOGIN:", r.text)

# VERIFICA UTENTE
r = session.get(url + "/api/utente")
print("STATO UTENTE:", r.text)

# LOGOUT
r = session.get(url + "/api/logout")
print("LOGOUT:", r.text)

# VERIFICA DOPO LOGOUT
r = session.get(url + "/api/utente")
print("STATO UTENTE:", r.text)
