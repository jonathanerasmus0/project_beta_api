from django.contrib import admin
from .models import CustomUser, Wallet, Account, Transaction
from django.contrib.auth.admin import UserAdmin

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

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('performed_by', 'transaction_type', 'currency', 'category', 'date_created', 'amount', 'transaction_id')
    search_fields = ('performed_by__username', 'performed_by__email', 'transaction_id')
    readonly_fields = ('date_created',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
