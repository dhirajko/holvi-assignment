from _decimal import Decimal
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from fintech.models import Account, Transaction
from fintech.serializers import UserSerializer, AccountSerializer, TransactionSerializer
from fintech.utility import AccountUtility, TranasactionUtility


account_utility=AccountUtility()
transaction_utility=TranasactionUtility()


#accounts/users
class UserDetails(APIView):

    # get detail of logged in user
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.user.is_staff:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            else:
                user = get_object_or_404(User, id=request.user.id)
                serializer = UserSerializer(user)
                return Response(serializer.data)


class AllAccountDetails(APIView):
    # accounts/accountDetails
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
        serialized_transactions=transaction_utility.serarch_transactions(request.user.id)
        return Response(serialized_transactions)

#accounts/transactions/<user_id>
class SelectedUsersTransactions(APIView):

    def get(self, request,user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('User Not logged in')
        if not (request.user.is_staff or request.user.id==user_id):
            return Response('Un authorized user')
        serialized_transactions=transaction_utility.serarch_transactions(user_id)
        return Response(serialized_transactions)


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
        return Response(serializer.data, status=HTTP_201_CREATED)



