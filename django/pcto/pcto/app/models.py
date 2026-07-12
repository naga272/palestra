from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BaseDataUser(AbstractUser):
    RUOLI = [
        ('STUD', 'Studente'),
        ('PROF', 'Professore'),
        ('SUPV', 'Supervisore'),
    ]
    ruolo = models.CharField(max_length=4, choices=RUOLI)
    codFiscale = models.CharField(max_length=16)
    DataNascita = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.username} ({self.get_ruolo_display()})"


class Azienda(models.Model):
    piva = models.CharField(max_length=16)
    nome = models.CharField(max_length=64)
    descrizione = models.TextField()

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Azienda"
        verbose_name_plural = "Aziende"


class Filiale(models.Model):
    azienda = models.ForeignKey(
        Azienda,
        on_delete=models.CASCADE,
        related_name="filiali"
    )
    via = models.CharField(max_length=64)
    n_civico = models.CharField(max_length=8)
    comune = models.CharField(max_length=32)
    citta = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.via} {self.n_civico}"

    class Meta:
        verbose_name = "Filiale"
        verbose_name_plural = "Filiali"


class SupervisoreAzienda(models.Model):
    user = models.OneToOneField(
        BaseDataUser,
        on_delete=models.CASCADE,
        related_name="SupervisoreAzienda"
    )
    filiale = models.ForeignKey(
        Filiale,
        on_delete=models.CASCADE,
        related_name="gestire"
    )

    def __str__(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        verbose_name = "SupervisoreAzienda"
        verbose_name_plural = "SupervisoreAzienda"


class Progetto(models.Model):
    supervisore = models.ForeignKey(
        SupervisoreAzienda,
        on_delete=models.CASCADE,
        related_name="progetti",
    )
    titolo = models.CharField(max_length=255)
    descrizione = models.TextField()
    requisiti = models.TextField(blank=True, null=True)
    tempo_stimato = models.IntegerField()
    is_completato = models.BooleanField(default=False)
    timestamp_creazione = models.FloatField(null=True, blank=True)
    n_posti_disp = models.IntegerField()

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"


class Studente(models.Model):
    user = models.OneToOneField(
        BaseDataUser,
        on_delete=models.CASCADE,
        related_name="studente"
    )

    progetto = models.ForeignKey(
        Progetto,
        on_delete=models.CASCADE,
        related_name="partecipare",
        blank=True,
        null=True
    )

    timestamp_presa_incarico_p = models.FloatField(null=True, blank=True)

    matricola = models.CharField(max_length=5)
    anno_scolastico = models.IntegerField()
    sezione = models.CharField(max_length=2)
    tot_ore_pcto = models.IntegerField()

    def __str__(self):
        return f"{self.matricola}"

    class Meta:
        verbose_name = "Studente"
        verbose_name_plural = "Studenti"


class StoricoProgettoStudente(models.Model):
    studente = models.ForeignKey(
        Studente,
        on_delete=models.CASCADE,
        related_name="ha_partecipato",
        blank=True,
        null=True
    )
    progetto = models.ForeignKey(
        Progetto,
        on_delete=models.CASCADE,
        related_name="progetto",
        blank=True,
        null=True
    )

    timestamp_abbandono = models.FloatField()

    def __str__(self):
        return f"{self.matricola}"

    class Meta:
        verbose_name = "StoricoProgettoStudente"
        verbose_name_plural = "StoricoProgettoStudente"


class Proff(models.Model):
    user = models.OneToOneField(
        BaseDataUser,
        on_delete=models.CASCADE,
        related_name="proff"
    )

    def __str__(self):
        return f"{self.nome}"

    class Meta:
        verbose_name = "Proff"
        verbose_name_plural = "Proff"


class Diario(models.Model):
    studente = models.ForeignKey(
        Studente,
        on_delete=models.CASCADE,
        related_name="diari"
    )
    professore = models.ForeignKey(
        Proff,
        on_delete=models.CASCADE,
        related_name="diari"
    )

    def __str__(self):
        return f"{self.studente.user.username}"

    class Meta:
        verbose_name = "Voce Diario"
        verbose_name_plural = "Voci Diario"


class PaginaDiario(models.Model):
    diario = models.ForeignKey(
        Diario,
        on_delete=models.CASCADE,
        related_name="pagine"
    )
    supervisore = models.ForeignKey(
        SupervisoreAzienda,
        on_delete=models.CASCADE,
        related_name="modifica"
    )

    contenuto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagina del {self.data}"

    class Meta:
        verbose_name = "Pagina Diario"
        verbose_name_plural = "Pagine Diario"
        ordering = ["-data"]
