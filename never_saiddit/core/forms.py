from django import forms


class AcceptanceForm(forms.Form):
    has_accepted = forms.BooleanField(
        widget=forms.HiddenInput(),
    )
