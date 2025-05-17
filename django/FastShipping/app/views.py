from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AddProdottoForm, OrdiniForm
from .models import BaseDataUser, Cliente, Negozio, Prodotto, Consegna, Ordini

from datetime import datetime, timedelta
import re


def homepage(request):
    return render(request, "index.html")


def validate_password(password, conf_psw):
    if password != conf_psw:
        return "Le password non coincidono"
    
    if len(password) < 8:
        return "La password deve contenere almeno 8 caratteri"
    
    if len(password) > 32:
        return "La password non può superare 32 caratteri"
    
    if not re.search(r"[a-z]", password):
        return "La password deve contenere almeno una lettera minuscola"
    
    if not re.search(r"[A-Z]", password):
        return "La password deve contenere almeno una lettera maiuscola"
    
    if not re.search(r"\d", password):
        return "La password deve contenere almeno un numero"
    
    if not re.search(r"[!£$%&()=?'\^*+\-_,;.:#@§]", password):
        return "La password deve contenere almeno un carattere speciale tra: !£$%&()=?'^*+-_,;.:#@§"
    
    return None


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            tipo_utente = form.cleaned_data["tipo_utente"]
            username = form.cleaned_data["username"]
            eta = form.cleaned_data["eta"]
            email = form.cleaned_data["email"]
            cap = form.cleaned_data["CAP"]
            citta = form.cleaned_data["citta"]
            indirizzo = form.cleaned_data["indirizzo"]
            password = form.cleaned_data["password1"]
            conf_psw = form.cleaned_data["password2"]

            # valida username univoco
            if BaseDataUser.objects.filter(username=username).exists():
                form.add_error('username', "Username già registrato")
                return render(request, "register.html", {"form": form})

            # valida CAP (5 cifre)
            if not re.fullmatch(r"\d{5}", cap):
                form.add_error('CAP', "CAP non valido, deve contenere 5 cifre")
                return render(request, "register.html", {"form": form})

            # valida età (0-100)
            if tipo_utente != "azienda": 
                if eta < 0 or eta > 100:
                    form.add_error('eta', "Età non valida, deve essere tra 0 e 100")
                    return render(request, "register.html", {"form": form})


            # valida password
            psw_error = validate_password(password, conf_psw)
            if psw_error:
                form.add_error('password1', psw_error)
                return render(request, "register.html", {"form": form})


            # valida azienda
            if tipo_utente == "azienda":
                nome_azienda = form.cleaned_data["nome_azienda"]
                p_iva = form.cleaned_data["p_iva"]

                if not nome_azienda:
                    form.add_error('nome_azienda', "Il nome azienda è obbligatorio")
                    return render(request, "register.html", {"form": form})

                if len(nome_azienda) > 256:
                    form.add_error('nome_azienda', "Il nome azienda non può superare 256 caratteri")
                    return render(request, "register.html", {"form": form})

                if not p_iva:
                    form.add_error('p_iva', "La partita IVA è obbligatoria")
                    return render(request, "register.html", {"form": form})

                if not re.fullmatch(r"\d{11}", p_iva):
                    form.add_error('p_iva', "Partita IVA non valida, deve contenere 11 cifre")
                    return render(request, "register.html", {"form": form})

                if Negozio.objects.filter(p_iva=p_iva).exists():
                    form.add_error('p_iva', "Partita IVA già registrata")
                    return render(request, "register.html", {"form": form})

            user = BaseDataUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            if tipo_utente == "azienda":
                Negozio.objects.create(
                    user=user,
                    p_iva=p_iva,
                    nome_azienda=nome_azienda,
                    indirizzo=indirizzo,
                    cap=cap,
                    citta=citta
                )

            else:
                Cliente.objects.create(
                    user=user,
                    eta=eta,
                    indirizzo=indirizzo,
                    cap=cap,
                    citta=citta
                )

            # login automatico
            login(request, user)
            return redirect("profile")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    
    try:
        # caso negozio
        negozio = user.negozio
        prodotti = list(negozio.prodotti.all())

        context = {
            "all_products" : prodotti,
            "user" : {
                "tipo_utente": "azienda",
                "username": user.username,
                "email": user.email,
                "nome_azienda": negozio.nome_azienda,
                "p_iva": negozio.p_iva,
                "indirizzo": negozio.indirizzo,
                "citta": negozio.citta,
                "cap": negozio.cap
            }
        }
    except Negozio.DoesNotExist:
        # caso in cui e' cliente
        try:
            cliente = user.cliente
            buy_product = Prodotto.objects.all()

            ordini_cliente = Ordini.objects.filter(cliente_id=cliente)

            context = {
                "user": {
                    "tipo_utente": "cliente",
                    "username": user.username,
                    "email": user.email,
                    "eta": cliente.eta,
                    "indirizzo": cliente.indirizzo,
                    "citta": cliente.citta,
                    "cap": cliente.cap,
                },
                "buy_product" : buy_product,
                "ordini_cliente" : ordini_cliente
            }
        except Cliente.DoesNotExist:
            # Se non è né negozio né cliente
            return redirect("login")

    return render(request, "profile.html", context)


# campi AddProdottoForm
# ["nome_prod", "bio_prod", "quantita", "cons_domicilio", "ritiro_conv", "ritiro_lock"]

@login_required
def widget(request):
    user = request.user

    if request.method == "POST":
        form = AddProdottoForm(request.POST)
        if form.is_valid():
            prodotto = form.save(commit=False)
            prodotto.negozio = user.negozio
            prodotto.datetime = datetime.now() 
            prodotto.save()
        return redirect("profile")

    # GESTIONE RICHIESTA GET
    try:
        negozio = user.negozio
        form = AddProdottoForm()
        context = {
            "tipo_utente": "azienda",
            "form" : form,
            "user" : {
                "username": user.username,
                "email": user.email,
                "nome_azienda": negozio.nome_azienda,
                "p_iva": negozio.p_iva,
                "indirizzo": negozio.indirizzo,
                "citta": negozio.citta,
                "cap": negozio.cap
            }
        }
    except Negozio.DoesNotExist:
        # Se non è negozio, verifica se è cliente
        try:
            cliente = user.cliente
            context = {
                "tipo_utente": "cliente",
                "form" : form,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "eta": cliente.eta,
                    "indirizzo": cliente.indirizzo,
                    "citta": cliente.citta,
                    "cap": cliente.cap
                }
            }
        except Cliente.DoesNotExist:
            # Se non è né negozio né cliente
            return redirect('login')

    return render(request, "widget.html", context)


@login_required
def widget_info(request, num):
    user = request.user
    prodotto = Prodotto.objects.get(id=num)
    context = {
        "formAcquisto": OrdiniForm(),
        "prodotto": prodotto,
        "negozio": Negozio.objects.get(id=prodotto.negozio_id)
    }

    if request.method == "POST":
        form = OrdiniForm(request.POST)
        if form.is_valid():
            try:
                cliente = user.cliente
            except Cliente.DoesNotExist:
                return redirect("login")

            cons_domicilio = form.cleaned_data["cons_domicilio"]
            ritiro_conv = form.cleaned_data["ritiro_conv"]
            ritiro_lock = form.cleaned_data["ritiro_lock"]
            quantita = form.cleaned_data["quantita"]

            if quantita > prodotto.quantita:
                msg = "inserisci una quantita uguale o inferiore a quella proposta"
                form.add_error("quantita", msg)

            prodotto.quantita -= quantita
            prodotto.save()

            if not any([cons_domicilio, ritiro_conv, ritiro_lock]):
                msg = "Spunta almeno una di queste opzioni"
                form.add_error("cons_domicilio", msg)
                form.add_error("ritiro_conv", msg)
                form.add_error("ritiro_lock", msg)
                context["formAcquisto"] = form
                return render(request, "get_info_product.html", context)

            ordine              = form.save(commit=False)
            ordine.cliente      = cliente
            ordine.prodotto     = prodotto
            ordine.data_ordine  = datetime.now()

            ordine.importo = prodotto.importo * ordine.quantita

            if cons_domicilio:
                ordine.modalita = "domicilio"
                ordine.via = cliente.indirizzo
            
            elif ritiro_conv:
                ordine.modalita = "convenzionato"
                ordine.via = form.cleaned_data["ritiro_conv_addr"]

            elif ritiro_lock:
                ordine.modalita = "locker"
                ordine.via = form.cleaned_data["ritiro_lock_addr"]

            ordine.save()

            Consegna.objects.create(
                data_stimata = ordine.data_ordine + timedelta(days=2),
                tracking_id = ordine.id
            ).save()

            return redirect("profile")

        else:
            print("errore nella richiesta di tipo POST")
            print(form.errors)
            context["formAcquisto"] = form
            return render(request, "get_info_product.html", context)

    return render(request, "get_info_product.html", context)