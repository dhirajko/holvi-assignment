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
            if request.user.is_staff:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                user = get_object_or_404(User, id=request.user.id)
                serializer = UserSerializer(user)
                return Response(serializer.data)


class AllAccountDetails(APIView):

    # return all account of current user
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                print('staff')
                accounts = Account.objects.all()
                serializer = AccountSerializer(accounts, many=True)
                return Response(serializer.data)
            else:
                account = Account.objects.get(user_id=request.user.id)
                serializer = AccountSerializer(account)
                return Response(serializer.data)
        else:
            return Response('User Not logged in')

    # create new Account
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            name = request.data['name']
            balance = request.data['balance']
            user_id = request.data['user_id']
            user = get_object_or_404(User, id=user_id)
            account = Account(name=name, balance=balance, user=user)
            account.save()
            return Response(AccountSerializer(account).data)
        else:
            return Response('UnAuthorized to call this api')


class SelectedAccountDetail(APIView):

    # return selected account of logged user
    def get(self, request, ac_uuid, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                account = Account.objects.get(uuid=ac_uuid)
                serializer = AccountSerializer(account)
                return Response(serializer.data['balance'])
            else:
                account = get_object_or_404(Account, uuid=ac_uuid, user_id=request.user.id)
                serializer = AccountSerializer(account)
                return Response(serializer.data['balance'])
        else:
            return Response('User Not logged in ')


class AllTransactions(APIView):
    # return all the active transaction of logged in user ( all accounts)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            accounts = Account.objects.all().filter(user_id=request.user.id)

            for account in accounts:
                serializer = AccountSerializer(account)
                account_id = serializer.data['uuid']
                transactions = Transaction.objects.all().filter(account_id=account_id, active=True)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data)
        else:
            return Response('User Not logged in')

    # for creating new transaction
    def post(self, request, *args, **kwargs):  # still working on this
        if request.user.is_authenticated:
            account = Account.objects.get(user_id=request.user.id)

            transaction_date = request.data['transaction_date']
            amount = request.data['amount']
            description = request.data['description']
            active = request.data['active']

            new_balance = Decimal(account.balance) - Decimal(amount)

            if (new_balance >= 0):
                new_Transaction = Transaction(transaction_date=transaction_date,
                                              amount=amount,
                                              description=description,
                                              active=active,
                                              account=account)
                new_Transaction.save()
                print(new_balance)

                Account.objects.filter(uuid=account.uuid).update(balance=new_balance)
                if (active):
                    return Response(TransactionSerializer(new_Transaction).data)
                else:
                    return Response('Transaction saved')
            return Response(' Insufficient Balance')
        else:
            return Response('User Not logged in')


class SelectedUsersTransactions(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            accounts = Account.objects.all().filter(user_id=self.kwargs['id'])

            for account in accounts:
                serializer = AccountSerializer(account)
                account_id = serializer.data['uuid']
                transactions = Transaction.objects.all().filter(account_id=account_id, active=True)
                serializer = TransactionSerializer(transactions, many=True)
                return Response(serializer.data)
        else:
            return Response('User is not staff')

