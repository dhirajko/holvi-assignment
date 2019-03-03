from django.urls import path

from fintech.views import UserList, AccountDetail, AccountListCreateView

urlpatterns = [

    path('users', UserList.as_view(), name='accounts'),
    path('create', AccountListCreateView.as_view(), name='account_list'),
    path('<ac_uuid>', AccountDetail.as_view(), name='account_detail'),
]
