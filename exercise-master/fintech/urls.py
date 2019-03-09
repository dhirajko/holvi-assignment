from django.urls import path

from fintech.views import AllAccountDetails, SelectedAccountDetail, AllTransactions, UserDetails,SelectedUsersTransactions

urlpatterns = [

    path('users', UserDetails.as_view(), name='accounts'),
    path('accountDetails', AllAccountDetails.as_view(), name='account_list'),
    path('<ac_uuid>/balance', SelectedAccountDetail .as_view(), name='selected_account_detail'),
    path('transactions', AllTransactions.as_view(), name='own_transacton_list'),
    path('transactions/<id>', SelectedUsersTransactions.as_view(), name='any_transaction_list'),
]
