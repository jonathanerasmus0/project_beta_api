from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'AdminUser'),
        ('paid', 'PaidUser'),
        ('free', 'FreeUser'),
        ('accountant', 'Accountant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='free')

class Wallet(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date_opened = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('credit', 'Credit'),
    )
    TIERS = (
        ('tier1', 'Tier1'),
        ('tier2', 'Tier2'),
        ('tier3', 'Tier3'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=10)
    tier = models.CharField(max_length=10, choices=TIERS)
    accountant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='opened_accounts', on_delete=models.SET_NULL, null=True)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )
    CATEGORIES = (
        ('payments', 'Payments'),
        ('withdrawals', 'Withdrawals'),
        ('deposits', 'Deposits'),
        ('giftcards', 'Giftcards'),
    )
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    currency = models.CharField(max_length=10)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
