from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from fintech.models import Account


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name')


class AccountSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = ('uuid', 'name', 'balance', 'user')



