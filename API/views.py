from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Account, Transaction
from .serializers import WalletSerializer, AccountSerializer, TransactionSerializer
from .permissions import IsAdminUser, IsPaidUser, IsFreeUser, IsAccountant
from .utils import convert_currency, CurrencyConversionException
from .forms import CurrencyConversionForm
from django.utils import timezone
from decimal import Decimal
from rest_framework.decorators import action

# API Views
class APIRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        endpoints = {
            'Token Obtain Pair': reverse('token_obtain_pair', request=request),
            'Token Refresh': reverse('token_refresh', request=request),
            'Wallets': reverse('wallet-list', request=request),
            'Accounts': reverse('account-list', request=request),
            'Transactions': reverse('transaction-list', request=request),
        }
        return render(request, 'api_root.html', {'endpoints': endpoints})

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Wallet.objects.filter(owner=self.request.user).exists():
            raise serializers.ValidationError("User already has a wallet.")
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def close_wallet(self, request, pk=None):
        wallet = self.get_object()
        wallet.is_closed = True
        wallet.date_closed = timezone.now()
        wallet.save()
        return Response({'status': 'wallet closed'})

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.user_type == 'accountant':
            raise serializers.ValidationError("Only accountants can open accounts.")
        serializer.save(accountant=self.request.user)

    def get_queryset(self):
        if self.request.user.user_type == 'free':
            return Account.objects.none()
        return super().get_queryset()

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']
        user = self.request.user

        if currency != user.account.currency:
            amount = convert_currency(amount, currency, user.account.currency)
            currency = user.account.currency

        if user.account.tier == 'tier1' and amount > Decimal('10000.00'):
            raise serializers.ValidationError("Tier1 users can't make transactions more than 10000.")

        serializer.save(performed_by=user, amount=amount, currency=currency)

def currency_conversion_view(request):
    form = CurrencyConversionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        from_currency = form.cleaned_data['from_currency']
        to_currency = form.cleaned_data['to_currency']
        try:
            converted_amount = convert_currency(amount, from_currency, to_currency)
            return redirect(reverse('currency_conversion_result') + f'?amount={amount}&from_currency={from_currency}&to_currency={to_currency}&converted_amount={converted_amount}')
        except CurrencyConversionException as e:
            return render(request, 'currency_conversion.html', {
                'form': form,
                'error': str(e.detail)
            })
    
    return render(request, 'currency_conversion.html', {'form': form})

def currency_conversion_result_view(request):
    amount = request.GET.get('amount')
    from_currency = request.GET.get('from_currency')
    to_currency = request.GET.get('to_currency')
    converted_amount = request.GET.get('converted_amount')

    return render(request, 'currency_conversion_result.html', {
        'amount': amount,
        'from_currency': from_currency,
        'to_currency': to_currency,
        'converted_amount': converted_amount
    })

# Front-end Views
def home_view(request):
    return render(request, 'home.html')

def wallet_view(request):
    return render(request, 'wallet.html')

def account_view(request):
    return render(request, 'account.html')

def transaction_view(request):
    return render(request, 'transaction.html')
