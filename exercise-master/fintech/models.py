import uuid

from django.db import models


class Account(models.Model):
    """
    Represents a bank account in the system.

    The users of Account and Transaction model should make sure that the
    following conditions are always True:
        account.balance == sum(
           t.amount for t in account.transactions.all() if t.active
        )
        account.balance >= 0
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    def __str__(self):
        return f'Account: {self.name} - {self.uuid}'


class Transaction(models.Model):
    """
    Records transactions on account. You can think of these as entries
    on account statement.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(
        Account, related_name='transactions',
        on_delete=models.PROTECT)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=20, blank=True, default='')

    # If active is False, the transaction should not be visible to the
    # customer in any way.
    active = models.BooleanField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
