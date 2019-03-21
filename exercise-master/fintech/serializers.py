from django.contrib.auth.models import User
from django.forms import UUIDField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from fintech.models import Account, Transaction


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class AccountSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = ('uuid', 'name', 'balance', 'user')
        allow_null = True


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('uuid', 'transaction_date', 'amount', 'description', 'active', 'account_id')
        allow_null = True