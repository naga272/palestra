from django.db import models
from django.forms import ModelForm
from datetime import datetime


"""
    nella sezione suite per admin i db hanno il nome che finiscono per 's'. 
    Per risolvere questo problema bisogna aggiungere ai modelli la classe Meta
"""

class MemoryDomande(models.Model):
    titolo      = models.CharField(max_length=100)
    content     = models.TextField()
    username    = models.CharField(max_length=100, default="None")
    password    = models.CharField(max_length=100, default="None")
    ukey        = models.CharField(max_length=100, default="None")
    pkey        = models.CharField(max_length=100, default="None")
    datetime    = models.CharField(max_length=100, default="None")
    class Meta:
        verbose_name = 'Domande'
        verbose_name_plural = 'Domande'

    def __str__(self):
        return f'{self.titolo}'


class MemoryRisposte(models.Model):
    content     = models.TextField()
    data        = models.DateField(default=datetime.now)
    username    = models.CharField(max_length=100, default="None")
    password    = models.CharField(max_length=100, default="None")
    ukey        = models.CharField(max_length=100, default="None")
    pkey        = models.CharField(max_length=100, default="None")
    token_id    = models.IntegerField()

    def __str__(self):
        return f'domanda numero: {self.token_id}'

    class Meta:
        verbose_name = 'Risposte'
        verbose_name_plural = 'Risposte'


class BanWord(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id} {self.word}'

    class Meta:
        db_table = 'BanWord' 
