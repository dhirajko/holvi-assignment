import datetime
import json
from _decimal import Decimal

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from fintech.models import Account, Transaction



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User(username='user1', email='test1@test.com', is_staff=True, is_active=True, is_superuser=True)
        self.user1.set_password('test_password')
        self.user1.save()
        self.user2 = User(username='user2', email='test2@test.com', is_staff=False, is_active=True, is_superuser=True)
        self.user2.set_password('test_password')
        self.user2.save()


        self.account_attributes1 = {
            'name': 'account_name',
            'balance': 10.5,
            'user': self.user1
        }
        self.account_attributes2 = {
            'name': 'account_name',
            'balance': 10.5,
            'user': self.user2
        }
        self.account1 = Account.objects.create(**self.account_attributes1)
        self.account2 = Account.objects.create(**self.account_attributes2)

        self.transactions_attributes1 = {
            'account': self.account1,
            'transaction_date': datetime.datetime.now(),
            'amount': 1.5,
            'description': 'test',
            'active': True
        }
        self.transactions_attributes2 = {
            'account': self.account2,
            'transaction_date': datetime.datetime.now(),
            'amount': 1.5,
            'description': 'test',
            'active': True
        }
        self.transaction1 = Transaction.objects.create(**self.transactions_attributes1)
        self.transaction2 = Transaction.objects.create(**self.transactions_attributes2)

    def test_user_login_GET(self):
        self.client.get('/admin/', follow=True)
        login = self.client.login(username='user1', password='test_password')
        self.assertTrue(login)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user1.pk)

    # authorized user logged in
    def test_user_detail_with_login_GET(self):
        login = self.client.login(username='user1', password='test_password')
        response = self.client.get(reverse('accounts'))
        resp=json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertEqual(resp['username'],self.user1.username)


    def test_user_detail_without_login_GET(self):
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response['Content-Type'], "application/json")
        resp = json.loads(response.content)
        self.assertEqual('User not logged in',resp['msg'])

    # test other user detail as by staff user
    def test_user_detail_with_id_by_staff_success(self):
        login = self.client.login(username='user1', password='test_password')
        response=self.client.get(reverse('accounts_by_id',args=[self.user2.id]))
        self.assertEqual(response.status_code,200)

    # test other user detail as by non_staff user
    def test_get_user_detail_fails_on_unauthorized_user(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('accounts_by_id', args=[self.user2.id]))
        self.assertEqual(response.status_code, 401)

    #test own accounts list
    def test_logged_in_user_can_list_account(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json")
        resp = json.loads(response.content)
        self.assertEqual(resp[0]['name'],self.account2.name)


    def test_get_account_list_fails_without_login(self):
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 403)
        resp = json.loads(response.content)
        self.assertEqual('User not logged in',resp['msg'])

    #test creating account by staff user
    def test_account_create_by_staff(self):
        login = self.client.login(username='user1', password='test_password')
        response=self.client.post(reverse('account_list'),
                                  {"name":"new_test_account","balance":50,"user":self.user2.id},
                                  content_type="application/json")
        self.assertEqual(response.status_code,201)
        resp = json.loads(response.content)
        self.assertEqual(resp['user'],self.user2.id)

    # test creating account by non_staff user
    def test_account_create_by_staff(self):
        login = self.client.login(username='user2', password='test_password')
        response=self.client.post(reverse('account_list'),
                                  {   'account': self.account1.uuid,
                                      'transaction_date': datetime.datetime.now(),
                                      'amount': 1.5,
                                      'description': 'test',
                                      'active': True
                                  },
                                  content_type="application/json")
        self.assertEqual(response.status_code,401)
        resp = json.loads(response.content)
        self.assertEqual(resp['msg'],'Unauthorized user')

    # test creating account of invalid user
    def test_account_create_by_non_staff(self):
        login = self.client.login(username='user1', password='test_password')
        response = self.client.post(reverse('account_list'),
                                    {"name": "new_test_account", "balance": 50, "user": 10},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)

    # test for checking balance of account
    def test_balacne_of_account(self):
        login = self.client.login(username='user1', password='test_password')
        response = self.client.get(reverse('selected_account_balance', args=[self.account2.uuid]))
        self.assertEqual(response.status_code, 200)

    # test for checking balance of invalid user
    def test_balace_of_other_by_non_staff(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('selected_account_balance', args=[self.account1.uuid]))
        self.assertEqual(response.status_code, 401)

    # test for checking balance of invalid account
    def test_balace_of_other_by_non_staff(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('selected_account_balance', args=['387da0a2-b8b4-4939-af91-555989304312']))
        self.assertEqual(response.status_code, 404)

    #check all transaction of own account
    def test_own_transactions(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('own_transacton_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json")
        resp = json.loads(response.content)
        self.assertEqual(Decimal(resp[0][0]['amount']), self.transaction1.amount)

    #test selected account transactions
    def test_selected_account_transactions_by_staff(self):
        login = self.client.login(username='user1', password='test_password')
        response = self.client.get(reverse('selected_account_transacton_list',args=[self.account2.uuid]))
        self.assertEqual(response.status_code,200)
        resp = json.loads(response.content)
        self.assertEqual(Decimal(resp[0]['amount']),self.transaction2.amount)

    # test selected account transactions by unauthorized user
    def test_selected_account_transactions_by_staff(self):
        login = self.client.login(username='user2', password='test_password')
        response = self.client.get(reverse('selected_account_transacton_list', args=[self.account1.uuid]))
        self.assertEqual(response.status_code, 401)
        resp = json.loads(response.content)
        self.assertEqual(resp['msg'],'Unauthorized user')

   # Test withdraw with enough balance
    def test_withdraw_with_enough_balance(self):
        login = self.client.login(username='user2', password='test_password')
        data={

            "transaction_date": "2019-03-26",
            "amount": 2.00,
            "description": "dsfasdf",
            "active": True,
            "account_id":self.account2.uuid
        }
        transaction_response = self.client.post(reverse('withdraw_transaction'),data,content_type="application/json")
        balance_response=self.client.get(reverse('selected_account_balance',args=[self.account2.uuid]))
        resp_transaction=json.loads(transaction_response.content)
        resp_balance=json.loads(balance_response.content)
        self.assertEqual(transaction_response.status_code,200)
        self.assertEqual(balance_response.status_code,200)
        self.assertEqual(Decimal(resp_transaction['amount']),data['amount'])
        self.assertEqual(Decimal(resp_balance),8.50)

# Test withdraw without enough balance
    def test_withdraw_with_enough_balance(self):
        login = self.client.login(username='user2', password='test_password')
        data={

            "transaction_date": "2019-03-26",
            "amount": 12.00,
            "description": "dsfasdf",
            "active": True,
            "account_id":self.account2.uuid
        }
        transaction_response = self.client.post(reverse('withdraw_transaction'),data,content_type="application/json")
        balance_response=self.client.get(reverse('selected_account_balance',args=[self.account2.uuid]))
        resp_balance=json.loads(balance_response.content)
        self.assertEqual(transaction_response.status_code,412)
        self.assertEqual(balance_response.status_code,200)
        self.assertEqual(Decimal(resp_balance),10.5)

# Test withdraw by unauthorized user or non staff
    def test_withdraw_with_enough_balance(self):
        login = self.client.login(username='user2', password='test_password')
        data={

            "transaction_date": "2019-03-26",
            "amount": 1.00,
            "description": "dsfasdf",
            "active": True,
            "account_id":self.account1.uuid
        }
        transaction_response = self.client.post(reverse('withdraw_transaction'),data,content_type="application/json")
        balance_response=self.client.get(reverse('selected_account_balance',args=[self.account1.uuid]))
        resp_balance=json.loads(balance_response.content)
        self.assertEqual(transaction_response.status_code,401)
        self.assertEqual(balance_response.status_code,401)
        self.assertEqual(Decimal(resp_balance),10.5)

# Test withdraw request to invalid  account number
    def test_withdraw_with_enough_balance(self):
        login = self.client.login(username='user1', password='test_password')
        invalid_uuid='387da0a2-b8b4-4939-af91-555989304312'
        data={

            "transaction_date": "2019-03-26",
            "amount": 1.00,
            "description": "dsfasdf",
            "active": True,
            "account_id": invalid_uuid
        }
        transaction_response = self.client.post(reverse('withdraw_transaction'),data,content_type="application/json")
        balance_response=self.client.get(reverse('selected_account_balance',args=[invalid_uuid]))
        self.assertEqual(transaction_response.status_code,404)
        self.assertEqual(balance_response.status_code,404)


  # Test deposit balance
    def test_withdraw_with_enough_balance(self):
        login = self.client.login(username='user1', password='test_password')
        data={

            "transaction_date": "2019-03-26",
            "amount": 2.00,
            "description": "dsfasdf",
            "active": True,
            "account_id":self.account2.uuid
        }
        transaction_response = self.client.post(reverse('deposit_transaction'),data,content_type="application/json")
        balance_response=self.client.get(reverse('selected_account_balance',args=[self.account2.uuid]))
        resp_balance=json.loads(balance_response.content)
        self.assertEqual(transaction_response.status_code,201)
        self.assertEqual(balance_response.status_code,200)
        self.assertEqual(Decimal(resp_balance),12.50)

