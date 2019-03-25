from django.urls import path

from fintech.views import AccountList, SelectedAccountBalance, AllTransactions, UserDetails, WithdrawView,DepositView,SelectedUsersTransactions,SelectedAccountTransactions,SelectedUserDetails,UserAccount

urlpatterns = [

    path('user', UserDetails.as_view(), name='accounts'),
    path('user/<user_id>', SelectedUserDetails.as_view(), name='accounts_by_id'),

    path('accounts', AccountList.as_view(), name='account_list'),
    path('<user_id>/accounts', UserAccount .as_view(), name='selected_user_account_detail'),
    path('<ac_uuid>/balance', SelectedAccountBalance .as_view(), name='selected_account_balance'),

    path('transactions', AllTransactions.as_view(), name='own_transacton_list'),
    path('<ac_uuid>/transactions', SelectedAccountTransactions.as_view(), name='selected_account_transacton_list'),
    path('<user_id>/accounts/transactions', SelectedUsersTransactions.as_view(), name='selected_user_transaction_list'),
    path('user/account/withdraw',WithdrawView.as_view(),name='withdraw_transaction'),
    path('user/account/deposit',DepositView.as_view(),name='deposit_transaction')

]