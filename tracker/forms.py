from django import forms
from .models import country


class countryForm(forms.ModelForm):
    class Meta:
        model = country
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Country Name'
            }),
        }