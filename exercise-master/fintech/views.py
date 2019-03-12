from _decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from fintech.models import Account, Transaction
from fintech.serializers import UserSerializer, AccountSerializer, TransactionSerializer
from fintech.utility import AccountUtility, TranasactionUtility,LogTranaction


account_utility=AccountUtility()
transaction_utility=TranasactionUtility()
post_log_file=LogTranaction('post_log_file')

#accounts/users
class UserDetails(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User not logged in')
        users = get_object_or_404(User,id=request.user.id)
        serializer = UserSerializer(users)
        return Response(serializer.data)


#accounts/users/<user_id>
class SelectedUserDetails(APIView):

    def get(self, request,user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User not logged in')
        if not request.user.is_staff:
            return Response('Only staff can view account for customer')
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)



# accounts/accountDetails
class AllAccountDetails(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        serialized_accounts=account_utility.search_account(request.user.id)
        return Response(serialized_accounts)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User must be logged in')
        if not request.user.is_staff:
            return Response('Only staff can create account for customer')
        user = get_object_or_404(User, id=request.user.id)
        serializer = AccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages)
        serializer.save(user=user)
        post_log_file.post_log('create user',request.user.id,serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)


# accounts/accountDetails/<user_id>
class SelectedAccountDetails(APIView):

    def get(self, request,user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        if not(request.user.is_staff or request.user.id==user_id):
            return Response('Un authorized user')
        serialized_accounts=account_utility.search_account(user_id)
        return Response(serialized_accounts)




#<ac_uuid>/balance
class SelectedAccountDetail(APIView):

    def get(self, request, ac_uuid, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in ')
        if not request.user.is_staff:
            account = get_object_or_404(Account, uuid=ac_uuid, user_id=request.user.id)
            serializer = AccountSerializer(account)
            return Response(serializer.data['balance'])
        account = Account.objects.get(uuid=ac_uuid)
        serializer = AccountSerializer(account)
        return Response(serializer.data['balance'])



#accounts/transactions
class AllTransactions(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        serialized_transactions=transaction_utility.serarch_transactions_by_user_id(request.user.id)
        return Response(serialized_transactions)


#accounts/transactions/<user_id>
class SelectedUsersTransactions(APIView):

    def get(self, request,user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        if not (request.user.is_staff or request.user.id==user_id):
            return Response('Un authorized user')
        serialized_account=transaction_utility.serarch_transactions_by_user_id(user_id)
        return Response(serialized_account)



#accounts/<ac_id>/transactions
class SelectedAccountTransactions(APIView):

    def get(self, request,ac_uuid, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        account=get_object_or_404(Account,uuid=ac_uuid)
        print('I am here')
        if not (request.user.is_staff or request.user.id==account.user):
            return Response('Un authorized user')
        transactions = Transaction.objects.filter(account=account, active=True)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)



# /accounts/<account_id>/withdraw
class WithdrawView(APIView):

    @transaction.atomic()
    def post(self, request, account_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User must be logged in')
        account = get_object_or_404(Account, uuid=account_id)
        print(account.uuid)
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.error_messages)
        new_balance = Decimal(account.balance) - Decimal(request.data['amount'])
        if new_balance <= 0:
            return Response('Not enough balance to withdraw')
        serializer.save(account=account)
        account.balance = new_balance
        account.save()
        post_log_file.post_log('withdraw',request.user.id,serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)


# /accounts/<account_id>/deposit
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
        post_log_file.post_log('Deposit',request.user.id,serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED)



