import datetime
import json
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from fintech.models import Account, Transaction
from fintech.serializers import AccountSerializer, TransactionSerializer, UserSerializer


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User(username='test1', email='test1@test.com', is_staff=True, is_active=True, is_superuser=True)
        self.user1.set_password('test_password')
        self.user1.save()
        self.user2 = User(username='test2', email='test2@test.com', is_staff=False, is_active=True, is_superuser=True)
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

        self.serialized_user1 = UserSerializer(self.user1)
        self.serialized_user2 = UserSerializer(self.user2)
        self.serialized_account1 = AccountSerializer(self.account1)
        self.serialized_account2 = AccountSerializer(self.account2)
        self.serialized_transaction1 = TransactionSerializer(self.transaction1)
        self.serialized_transaction2 = TransactionSerializer(self.transaction2)

    def test_user_login_GET(self):
        self.client.get('/admin/', follow=True)
        login = self.client.login(username='test1', password='test_password')
        self.assertTrue(login)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user1.pk)

    # authorized user logged in
    def test_user_detail_GET(self):
        self.client.get('/admin/', follow=True)
        login = self.client.login(username='test1', password='test_password')
        response = self.client.get(reverse('accounts'))
        if login:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], "application/json")
            resp = json.loads(response.content)
            self.assertEqual(resp['id'], self.serialized_user1.data['id'])
        else:
            response_content = json.loads(response.content)
            self.assertEqual(response_content, 'User not logged in')

    # Test selected user
    def test_selected_user_details_GET(self):
        self.client.get('/admin/', follow=True)
        args_id = 1;
        login = self.client.login(username='test2', password='test_password')
        response = self.client.get(reverse('selected_user_account_detail', args=[args_id]))
        resp = json.loads(response.content)

        if login:
            id = int(self.client.session['_auth_user_id'])
            user = get_object_or_404(User, id=id)

            if user.is_staff or id == args_id:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['Content-Type'], "application/json")
                self.assertEqual(resp[0]['user'], self.serialized_user2.data['id'])

            else:
                self.assertEqual(resp, 'Unauthorized user')

        else:
            self.assertEqual(resp, 'User not logged in')

    # test accountList
    def test_selected_user_details_GET(self):
        self.client.get('/admin/', follow=True)
        login = self.client.login(username='test1', password='test_password')
        response = self.client.get(reverse('account_list'))
        resp = json.loads(response.content)

        if login:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], "application/json")
            self.assertEqual(resp[0], self.serialized_account1.data)

        else:
            self.assertEqual(resp, 'User not logged in')

    # test for post in account_list
    def test_selected_user_details_POST(self):
        self.client.get('/admin/', follow=True)
        account_holder_id = 100
        login = self.client.login(username='test1', password='test_password')
        response = self.client.post(reverse('account_list'),
                                    {"name": "test Saving", "balance": "100.00", "user": account_holder_id})
        resp = json.loads(response.content)

        id = int(self.client.session['_auth_user_id'])
        user = get_object_or_404(User, id=id)

        if login:
            if user.is_staff:



                    self.assertEqual(get_object_or_404(User,account_holder_id),resp[0] )
                    self.assertEqual(response['Content-Type'], "application/json")



            else:
                self.assertEqual(resp, 'Only staff can create account for customer')

        else:
            self.assertEqual(resp, 'User not logged in')
