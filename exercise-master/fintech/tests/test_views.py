import datetime
import json
from django.contrib.auth.models import User
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
        self.account2=Account.objects.create(**self.account_attributes2)

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
        self.transaction2=Transaction.objects.create(**self.transactions_attributes2)

        self.serialized_user1 = UserSerializer(self.user1)
        self.serialized_user2=UserSerializer(self.user2)
        self.serialized_account1 = AccountSerializer(self.account1)
        self.serialized_account2=AccountSerializer(self.account2)
        self.serialized_transaction1= TransactionSerializer(self.transaction1)
        self.serialized_transaction2 = TransactionSerializer(self.transaction2)





    def test_user_login_GET(self):
        self.client.get('/admin/', follow=True)
        login=self.client.login(username='test1', password='test_password')
        self.assertTrue(login)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user1.pk)

    #authorized user logged in
    def test_user_detail_GET(self):
        self.client.get('/admin/', follow=True)
        login=self.client.login(username='test1', password='test_password')
        response = self.client.get(reverse('accounts'))
        if login:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], "application/json")
            resp = json.loads(response.content)
            self.assertEqual(resp['id'], self.serialized_user1.data['id'])
        else:
            response_content = json.loads(response.content)
            self.assertEqual(response_content, 'User not logged in')






