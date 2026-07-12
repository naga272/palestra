from django import forms
from .models import Progetto, PaginaDiario


class NewProgetto(forms.ModelForm):
    class Meta:
        model = Progetto
        fields = [
            "titolo",
            "descrizione",
            "requisiti",
            "tempo_stimato"
        ]
        labels = {
            "tempo_stimato": "Tempo stimato in ore:",
        }


class NewPagina(forms.ModelForm):
    class Meta:
        model = PaginaDiario

        fields = [
            "contenuto",
        ]
        labels = {
            "contenuto": "Spiega che cosa ha fatto oggi questo studente",
        }
