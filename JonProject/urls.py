from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import WalletViewSet, AccountViewSet, TransactionViewSet, APIRootView, currency_conversion_view, currency_conversion_result_view, home_view, wallet_view, wallet_edit_view, wallet_delete_view, account_view, account_edit_view, account_delete_view, transaction_view, transaction_edit_view, transaction_delete_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'wallets', WalletViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', home_view, name='home'),
    path('wallet/', wallet_view, name='wallet'),
    path('wallet/edit/<int:pk>/', wallet_edit_view, name='wallet_edit'),
    path('wallet/delete/<int:pk>/', wallet_delete_view, name='wallet_delete'),
    path('account/', account_view, name='account'),
    path('account/edit/<int:pk>/', account_edit_view, name='account_edit'),
    path('account/delete/<int:pk>/', account_delete_view, name='account_delete'),
    path('transaction/', transaction_view, name='transaction'),
    path('transaction/edit/<int:pk>/', transaction_edit_view, name='transaction_edit'),
    path('transaction/delete/<int:pk>/', transaction_delete_view, name='transaction_delete'),
    path('currency-conversion/', currency_conversion_view, name='currency_conversion'),
    path('currency-conversion-result/', currency_conversion_result_view, name='currency_conversion_result'),
]
