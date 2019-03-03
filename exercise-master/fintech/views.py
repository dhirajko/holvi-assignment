from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from fintech.models import Account
from fintech.serializers import UserSerializer, AccountSerializer


# Create your views here.


class UserList(APIView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        # Many = true when we have to serialize many
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class AccountListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, id=request.data['user'])
            serializer.save(user=user)
            return Response(serializer.data, status=HTTP_201_CREATED)


class AccountDetail(APIView):
    def get(self, request, ac_uuid, **kwargs):
        account = get_object_or_404(Account, uuid=ac_uuid)
        serializer = AccountSerializer(account)
        return Response(serializer.data)
