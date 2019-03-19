import datetime

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from fintech.models import Account, Transaction
from fintech.serializers import AccountSerializer, TransactionSerializer


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='test', email='test@test.com', is_staff=True, is_active=True, is_superuser=True)
        self.user.save()
        self.account_attributes = {
            'name': 'account_name',
            'balance': 10.5,
            'user': self.user
        }

        self.account = Account.objects.create(**self.account_attributes)
        self.account_serializer = AccountSerializer(instance=self.account)

        self.transactions_attributes = {
            'account': self.account,
            'transaction_date': datetime.datetime.now(),
            'amount': 1.5,
            'description': 'test',
            'active': True
        }

        self.transaction = Transaction.objects.create(**self.transactions_attributes)
        self.transaction_serializer = TransactionSerializer(self.transaction)

    def test_user_details_GET(self):
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)
        self.client.login(username='test', password='test_password')

