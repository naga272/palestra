from django import forms


class Tracking(forms.Form):
    chiaveConsegna = forms.UUIDField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'inserisci chiave'
            }
        )
    )
