from django import forms
from captcha.fields import CaptchaField  # lo uso per il captcha


class FormDomanda(forms.Form):
    titolo = forms.CharField()
    contenuto = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder" : "Esponi il tuo problema!"
        })
    )
    username = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()


class FormRisposta(forms.Form):
    contenuto = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder" : "Rispondi qui alla domanda!",
        'style': 'white-space: pre-wrap',
        'class' : "scrivi"
    }))

    username = forms.CharField()
    password = forms.CharField()