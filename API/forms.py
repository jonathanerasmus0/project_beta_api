# forms.py
from django import forms

class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    from_currency = forms.CharField(max_length=10)
    to_currency = forms.CharField(max_length=10)
