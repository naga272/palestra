from django import forms
from .models import *


class RegisterForm(forms.Form):    
    USER_TYPE = (
        ('cliente', 'Cliente'),
        ('azienda', 'Azienda'),
    )

    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    eta = forms.IntegerField(required=False)
    CAP = forms.CharField(required=True, max_length=5)
    citta = forms.CharField(required=True, max_length=64)
    indirizzo = forms.CharField(required=True, max_length=256)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    tipo_utente = forms.ChoiceField(choices=USER_TYPE)
    nome_azienda = forms.CharField(required=False, max_length=256)
    p_iva = forms.CharField(required=False, max_length=16)


class AddProdottoForm(forms.ModelForm):
    class Meta:
        model = Prodotto 
        fields = ["nome_prod", "bio_prod", "quantita", "importo"]


class OrdiniForm(forms.ModelForm):
    cons_domicilio = forms.BooleanField(required=False)
    ritiro_conv = forms.BooleanField(required=False)
    ritiro_lock = forms.BooleanField(required=False)
    ritiro_conv_addr = forms.ChoiceField(required=False, choices=VIE_X_CONV)
    ritiro_lock_addr = forms.ChoiceField(required=False, choices=VIE_X_LOCK)

    class Meta:
        model = Ordini
        fields = [
            "quantita", "cons_domicilio", "ritiro_conv", 
            "ritiro_conv_addr", "ritiro_lock", "ritiro_lock_addr"
        ] 

 