from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Account, Transaction
from .serializers import WalletSerializer, AccountSerializer, TransactionSerializer
from .permissions import IsAdminUser, IsPaidUser, IsFreeUser, IsAccountant
from .utils import convert_currency
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

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

        # Convert currency if needed
        if currency != user.account.currency:
            amount = convert_currency(amount, currency, user.account.currency)
            currency = user.account.currency

        if user.account.tier == 'tier1' and amount > 10000:
            raise serializers.ValidationError("Tier1 users can't make transactions more than 10000.")

        serializer.save(performed_by=user, amount=amount, currency=currency)
