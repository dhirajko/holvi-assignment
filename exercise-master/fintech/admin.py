from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User

from fintech.models import Account, Transaction

# Register your models here.

admin.site.register(Account)
admin.site.register(Transaction)