from django.urls import path
from .views import *

urlpatterns = [
    path('user/data', get_user_data),
    path('transaction/create', create_transaction),
    path('transaction/<int:pk>', TransactionDetail.as_view()),
    path('category', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('account', AccountList.as_view()),
    path('account/<int:pk>', AccountDetail.as_view()),
    path('register', RegisterAPI.as_view()),
]
