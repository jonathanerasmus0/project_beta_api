from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser, Wallet, Account, Transaction
from django.contrib.auth.admin import UserAdmin
from .utils import convert_currency

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'balance', 'date_opened', 'date_closed', 'is_closed')
    search_fields = ('owner__username', 'owner__email')
    readonly_fields = ('date_opened', 'date_closed')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('owner', 'account_type', 'date_created', 'currency', 'tier', 'accountant')
    search_fields = ('owner__username', 'owner__email')
    readonly_fields = ('date_created',)

class CurrencyConversionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    from_currency = forms.CharField(max_length=10)
    to_currency = forms.CharField(max_length=10)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('performed_by', 'transaction_type', 'currency', 'category', 'date_created', 'amount', 'transaction_id')
    search_fields = ('performed_by__username', 'performed_by__email', 'transaction_id')
    readonly_fields = ('date_created',)
    actions = ['convert_currency']

    def convert_currency(self, request, queryset):
        if 'apply' in request.POST:
            form = CurrencyConversionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_currency = form.cleaned_data['from_currency']
                to_currency = form.cleaned_data['to_currency']
                converted_amount = convert_currency(amount, from_currency, to_currency)
                self.message_user(request, f"Converted {amount} {from_currency} to {converted_amount} {to_currency}")
                return HttpResponseRedirect(request.get_full_path())
        else:
            form = CurrencyConversionForm(initial={
                'amount': queryset[0].amount,
                'from_currency': queryset[0].currency,
                'to_currency': 'USD',  # Default target currency, change as needed
            })
        
        return render(request, 'admin/currency_conversion.html', {'form': form, 'transactions': queryset})

    convert_currency.short_description = "Convert selected transactions"

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Account, AccountAdmin)
