from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class BaseDataUser(AbstractUser):
    # login base: username, email, password, ecc.
    pass


class Cliente(models.Model):
    user = models.OneToOneField(BaseDataUser, on_delete=models.CASCADE, related_name='cliente')
    eta = models.PositiveIntegerField()
    indirizzo = models.CharField(max_length=256)
    cap = models.CharField(max_length=8)
    citta = models.CharField(max_length=64)
    # indirizzo_consegna = models.CharField(max_length=256, blank=True, null=True)
 
    def __str__(self):
        return f"{self.user.username}"


class Negozio(models.Model):
    user = models.OneToOneField(BaseDataUser, on_delete=models.CASCADE, related_name='negozio')
    p_iva = models.CharField(max_length=16)
    nome_azienda = models.CharField(max_length=256)
    indirizzo = models.CharField(max_length=256)
    cap = models.CharField(max_length=8)
    citta = models.CharField(max_length=64)
    
    def __str__(self):
        return self.nome_azienda


class Prodotto(models.Model):
    negozio     = models.ForeignKey(Negozio, on_delete=models.CASCADE, related_name='prodotti')
    nome_prod   = models.CharField(max_length=64)
    bio_prod    = models.TextField()
    quantita    = models.PositiveIntegerField()
    datetime    = models.CharField(max_length=64)
    importo     = models.FloatField()


MODALITA_CONSEGNA = (
    ("domicilio", "Domicilio"),
    ("convenzionato", "Convenzionato"),
    ("locker", "Locker")
)


VIE_X_CONV = (
    ("via pluto 14", "via pluto 14"),
    ("via giorgio 17", "via giorgio 17")
)


VIE_X_LOCK = (
    ("via pippo 111", "via pippo 111"),
    ("via ravenna 23", "via ravenna 23")
)


class Ordini(models.Model):
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ordini")
    prodotto    = models.ForeignKey(Prodotto, on_delete=models.CASCADE, related_name="prodotto")
    data_ordine = models.CharField(max_length=255)
    importo     = models.FloatField()
    modalita    = models.CharField(max_length=32, choices=MODALITA_CONSEGNA)
    quantita    = models.PositiveIntegerField()
    via         = models.CharField(max_length=32)

    # consegna a domicilio, ritiro verso un locker e e ritiro convenzionato
    cons_domicilio      = models.BooleanField()
    ritiro_conv         = models.BooleanField()
    ritiro_lock         = models.BooleanField()



class Consegna(models.Model):
    tracking        = models.ForeignKey(Ordini, on_delete=models.CASCADE, related_name="consegna")
    data_stimata    = models.CharField(max_length=255)  

