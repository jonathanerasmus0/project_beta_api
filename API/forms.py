from django import forms
from .models import Wallet, Account, Transaction

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'currency', 'tier']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'currency', 'category', 'amount']

class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    from_currency = forms.CharField(max_length=10)
    to_currency = forms.CharField(max_length=10)
