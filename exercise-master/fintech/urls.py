from django.urls import path

from fintech.views import AllAccountDetails, SelectedAccountDetail, AllTransactions, UserDetails, WithdrawView,DepositView,SelectedAccountDetails,SelectedUsersTransactions

urlpatterns = [

    path('users', UserDetails.as_view(), name='accounts'),

    path('accountDetails', AllAccountDetails.as_view(), name='account_list'),
    path('accountDetails/<user_id>', SelectedAccountDetails .as_view(), name='selected_account_detail'),
    path('<ac_uuid>/balance', SelectedAccountDetail .as_view(), name='selected_account_balance'),

    path('transactions', AllTransactions.as_view(), name='own_transacton_list'),
    path('transactions/<user_id>', SelectedUsersTransactions.as_view(), name='any_user_transaction_list'),
    path('<account_id>/withdraw',WithdrawView.as_view(),name='withdraw_transaction'),
    path('<account_id>/deposit',DepositView.as_view(),name='deposit_transaction')

]
