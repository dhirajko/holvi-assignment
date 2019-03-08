from _decimal import Decimal
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from fintech.models import Account, Transaction
from fintech.serializers import UserSerializer, AccountSerializer, TransactionSerializer


# Create your views here.


class UserDetails(APIView):

    # get detail of logged in user
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)


class AllAccountDetails(APIView):

    # return all account of current user
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            accounts = Account.objects.all().filter(user_id=request.user.id)
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        else:
            return Response('User Not logged in')
    #create new Account
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            name = request.data['name']
            balance = request.data['balance']
            user = get_object_or_404(User,id=request.user.id)
            account=Account(name=name,balance=balance,user=user)
            account.save()

            return Response(AccountSerializer(account).data)
        else:
            return Response('User Not logged in')




class SelectedAccountDetail(APIView):

    # return selected account of logged user
    def get(self, request, ac_uuid, *args, **kwargs):
        if request.user.is_authenticated:
            account = get_object_or_404(Account, uuid=ac_uuid, user_id=request.user.id)
            serializer = AccountSerializer(account)
            return Response(serializer.data['balance'])
        else:
            return Response('User Not logged in')


class AllTransactions(APIView):

    # return all the transaction of logged in user ( all accounts)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            accounts = Account.objects.all().filter(user_id=request.user.id)

            for account in accounts:
                serializer = AccountSerializer(account)
                accountId = serializer.data['uuid']
                transactions = Transaction.objects.all().filter(account_id=accountId)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data)
        else:
            return Response('User Not logged in')

    # for creating new transaction
    def post(self, request, *args, **kwargs):                                       #still working on this
        if request.user.is_authenticated:

            accounts = Account.objects.all().filter(user_id=request.user.id)
            for account in accounts:
                serializedAccount = AccountSerializer(account)
                balance = Decimal(serializedAccount.data['balance'])
                transactionAmount = Decimal(request.data['amount'])

                if (balance >= transactionAmount):
                    # request.data['account_id'] = serializedAccount.data.get('uuid')

                    serializer = TransactionSerializer(data=request.data)
                    print(request.data, flush=True)

                    if serializer.is_valid():
                        print(serializer.data, flush=True)
                        # serializer.save()
                        # newBalance = balance - transactionAmount
                        # serializedAccount.update(balance=newBalance)
                        return Response(serializer.validated_data)
                    else:
                        return Response('seralize unvalid')
                else:
                    return Response('Balance in sufficient')
            return Response('No account found for transaction')

        else:
            return Response('User Not logged in')
