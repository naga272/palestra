from app.models import BaseDataUser, Clienti, Consegna
from datetime import date, timedelta
from django.contrib.auth.models import Group
import random


def create_users():
    staff = []

    operatore_group = Group.objects.get(name="Operatore")
    admin_group = Group.objects.get(name="Admin")

    for i in range(3):
        u = BaseDataUser.objects.create_user(
            username=f"operatore{i}",
            email=f"operatore{i}@test.com",
            password="test123",
            first_name=f"Op{i}",
            last_name="Staff",
            is_staff=True,
        )
        u.groups.add(operatore_group)
        staff.append(u)

    admin = BaseDataUser.objects.create_user(
        username="admin",
        email="admin@test.com",
        password="admin123",
        first_name="Admin",
        last_name="System",
        is_staff=True,
        is_superuser=True,
    )
    admin.groups.add(admin_group)

    return staff, admin


def create_clienti():
    clienti = []

    for i in range(10):
        baccount = BaseDataUser.objects.create_user(
            username=f"cliente{i}",
            email=f"cliente{i}@test.com",
            password="test123",
            first_name=f"cliente{i}",
            last_name="cliente",
            is_staff=False,
        )

        c = Clienti.objects.create(
            user=baccount,
            via=f"Via {i} Roma",
            comune="Trento",
            provincia="TN",
            telefono=f"33300000{i}"
        )
        clienti.append(c)
        c.save()

    return clienti


def create_consegne(clienti):
    consegne = []

    for i in range(25):
        stato = random.choice([1, 2, 3, 4, 5])

        data_ritiro = date.today() - timedelta(days=random.randint(0, 10))

        data_consegna = None
        if stato == 4:
            data_consegna = data_ritiro + timedelta(days=random.randint(1, 5))

        c = Consegna.objects.create(
            cliente=random.choice(clienti),
            dataRitiro=data_ritiro,
            dataConsegna=data_consegna,
            stato=stato
        )
        consegne.append(c)

        c.save()

    return consegne
