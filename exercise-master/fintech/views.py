from _decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from fintech.models import Account, Transaction
from fintech.serializers import UserSerializer, AccountSerializer, TransactionSerializer
from fintech.utility import AccountUtility, TranasactionUtility, LogTranaction

account_utility = AccountUtility()
transaction_utility = TranasactionUtility()
post_log_file = LogTranaction('post_log_file')


#user
class UserDetails(APIView):

    def get(self, request, *args, **kwargs):
        print(request.user.id)
        if not request.user.is_authenticated:
            return Response(data='User not logged in',status=403)
        users = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(users)
        return Response(serializer.data)


#user/<user_id>
class SelectedUserDetails(APIView):

    def get(self, request, user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in',status=403)
        if not request.user.is_staff:
            return Response(data='Only staff can view account for customer',status=401)
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=200)


#accounts
class AccountList(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in',status=403)
        serialized_accounts = account_utility.search_account(request.user.id)
        return Response(serialized_accounts)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in',status=403)
        if not request.user.is_staff:
            return Response(data='Only staff can view account for customer',status=401)

        user = get_object_or_404(User, id=request.data['user'])
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages)
        serializer.save(user=user)
        post_log_file.post_log('create user', request.user.id, serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)


#<user_id>/accounts
class UserAccount(APIView):

    def get(self, request, user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in',status=403)
        print(request.user.id)
        if not (request.user.is_staff or request.user.id == int(user_id)):
            return Response('Unauthorized user',status=401)
        serialized_accounts = account_utility.search_account(user_id)
        return Response(serialized_accounts)


#<ac_uuid>/balance
class SelectedAccountBalance(APIView):

    def get(self, request, ac_uuid, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in', status=403)
        if not request.user.is_staff:
            account = get_object_or_404(Account, uuid=ac_uuid, user_id=request.user.id)
            serializer = AccountSerializer(account)
            return Response(serializer.data['balance'])
        account = Account.objects.get(uuid=ac_uuid)
        serializer = AccountSerializer(account)
        return Response(serializer.data['balance'])


#transactions
class AllTransactions(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in', status=403)
        serialized_transactions = transaction_utility.serarch_transactions_by_user_id(request.user.id)
        return Response(serialized_transactions)


#<user_id>/accounts/transactions
class SelectedUsersTransactions(APIView):

    def get(self, request, user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in', status=403)
        if not (request.user.is_staff or request.user.id == int(user_id)):
            return Response('Unauthorized user',status=401)
        serialized_account = transaction_utility.serarch_transactions_by_user_id(user_id)
        return Response(serialized_account)


# <ac_uuid>/transactions
class SelectedAccountTransactions(APIView):

    def get(self, request, ac_uuid, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in', status=403)
        account = get_object_or_404(Account, uuid=ac_uuid)
        if not (request.user.is_staff or request.user.id == account.user.id):
            return Response('Unauthorized user', status=401)
        transactions = Transaction.objects.filter(account=account, active=True)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


# <account_id>/withdraw
class WithdrawView(APIView):

    @transaction.atomic()
    def post(self, request, account_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data='User not logged in', status=403)
        account = get_object_or_404(Account, uuid=account_id)
        print(account.uuid)
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages)
        new_balance = Decimal(account.balance) - Decimal(request.data['amount'])
        if new_balance <= 0:
            return Response('Not enough balance to withdraw',status=412)
        serializer.save(account=account)
        account.balance = new_balance
        account.save()
        post_log_file.post_log('withdraw', request.user.id, serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)


#<account_id>/deposit
class DepositView(APIView):

    @transaction.atomic()
    def post(self, request, account_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User must be logged in')
        account = get_object_or_404(Account, uuid=account_id)
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages)
        new_balance = Decimal(account.balance) + Decimal(request.data['amount'])
        serializer.save(account=account)
        account.balance = new_balance
        account.save()
        post_log_file.post_log('Deposit', request.user.id, serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)
