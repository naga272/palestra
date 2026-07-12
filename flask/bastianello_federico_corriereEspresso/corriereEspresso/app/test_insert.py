from app.popolamento import create_users, create_clienti, create_consegne


staff, admin = create_users()
clienti = create_clienti()
consegne = create_consegne(clienti)

print("Seed completato")
# print("Users:", len(users))
print("Clienti:", len(clienti))
print("Consegne:", len(consegne))
