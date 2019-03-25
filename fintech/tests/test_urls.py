from django.test import SimpleTestCase
from django.urls import reverse,resolve

from fintech.views import UserDetails, SelectedUserDetails, AccountList, UserAccount, AllTransactions, \
    SelectedAccountTransactions, SelectedUsersTransactions, WithdrawView, DepositView, SelectedAccountBalance


class TestUrls(SimpleTestCase):

    def test_user_url_resolved(self):
        url=reverse('accounts')
        self.assertEqual(resolve(url).func.view_class,UserDetails)

    def test_user_by_id_url_resolved(self):
        url = reverse('accounts_by_id',args=["1"])
        self.assertEqual(resolve(url).func.view_class, SelectedUserDetails)

    def test_account_list_url_resolved(self):
        url= reverse('account_list')
        self.assertEqual(resolve(url).func.view_class,AccountList )

    def test_selected_user_account_url_resolved(self):
        url=reverse('selected_user_account_detail',args=["1"])
        self.assertEqual(resolve(url).func.view_class,UserAccount )

    def test_selected_account_balance_url_resolved(self):
        url=reverse('selected_account_balance',args=["10"])
        self.assertEqual(resolve(url).func.view_class,SelectedAccountBalance)

    def test_own_transacton_list_url_resolved(self):
        url=reverse('own_transacton_list')
        self.assertEqual(resolve(url).func.view_class,AllTransactions)

    def test_selected_user_trasactions_url_resolved(self):
        url = reverse('selected_account_transacton_list', args=["1"])
        self.assertEqual(resolve(url).func.view_class, SelectedAccountTransactions)


    def test_selected_user_transaction_list_url_resolved(self):
        url = reverse('selected_user_transaction_list', args=["1"])
        self.assertEqual(resolve(url).func.view_class, SelectedUsersTransactions)

    def test_withdraw_transaction_url_resolved(self):
        url = reverse('withdraw_transaction')
        self.assertEqual(resolve(url).func.view_class, WithdrawView)

    def test_deposit_transaction_url_resolved(self):
        url = reverse('deposit_transaction')
        self.assertEqual(resolve(url).func.view_class, DepositView)

