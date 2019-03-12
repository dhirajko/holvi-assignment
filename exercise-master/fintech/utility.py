from django.shortcuts import get_object_or_404

from fintech.models import Account, Transaction
from fintech.serializers import AccountSerializer, TransactionSerializer


class AccountUtility:
    def search_account(self,user_id):
        accounts = Account.objects.all().filter(user_id=user_id)
        serialized_accounts = []
        for account in accounts:
            serializer = AccountSerializer(account)
            serialized_accounts.append(serializer.data)
        return serialized_accounts

class TranasactionUtility:
    def serarch_transactions_by_user_id(self,user_id):
        accounts = Account.objects.all().filter(user_id=user_id)
        serialized_transactions = []
        for account in accounts:
            transactions = Transaction.objects.filter(account=account, active=True)
            serializer = TransactionSerializer(transactions, many=True)
            serialized_transactions.append(serializer.data)
        return serialized_transactions

class LogTranaction:
    def __init__(self,filename):
        file=open(filename,"w")
        self.filename=filename

    def post_log(self,action,user_id,serializer):
        logFile = open(self.filename, "a")
        logFile.write('{} by User{} with {} \n'.format(action, user_id, serializer))
        logFile.close()