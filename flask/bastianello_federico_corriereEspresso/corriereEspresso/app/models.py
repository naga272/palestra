from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.


class BaseDataUser(AbstractUser):
    '''
    *   La consegna dice:
    *   cliente DEVE avere nome e indirizzo
    *   Per AbstractUser il campo first_name e last_name
    *   sono opzionali, quindi faccio una override
    '''
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)


class Clienti(models.Model):
    user = models.ForeignKey(
        BaseDataUser,
        related_name="estensione",
        on_delete=models.CASCADE
    )
    via = models.CharField(max_length=64, blank=False)
    comune = models.CharField(max_length=16, blank=False)
    provincia = models.CharField(max_length=2, blank=False)
    telefono = models.CharField(max_length=9, blank=False)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return f"{self.user.username}"


class Consegna(models.Model):
    class Stato(models.IntegerChoices):
        '''
        I possibili stati di una consegna sono:
        da ritirare
        in deposito
        in consegna
        consegnato in
        giacenza
        '''
        DA_RITIRARE = 1
        IN_DEPOSITO = 2
        IN_CONSEGNA = 3
        CONSEGNATO = 4
        GIACENZA = 5

    chiaveConsegna = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    cliente = models.ForeignKey(
        Clienti,
        related_name="appartiene",
        on_delete=models.PROTECT
    )

    dataRitiro = models.DateField(blank=False)
    dataConsegna = models.DateField(null=True, blank=True)
    stato = models.IntegerField(choices=Stato.choices)

    class Meta:
        verbose_name = "Consegna"
        verbose_name_plural = "Consegne"
        '''
        Ho trovato questa cosa molto carina:
        tramite models.Index e' possibile ottimizzare
        le query. In pratica al posto di scansionare
        tutta la tabella riga per riga,
        tramite l'indice e' possibile fare una ricerca logaritmica
        '''
        models.Index(fields=["chiaveConsegna", "dataRitiro"])

    def __str__(self):
        return f"{self.cliente.user.username} - stato: {self.stato}"
