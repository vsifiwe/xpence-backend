from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import *
from .models import *
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": "success"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user, token = response
    user_id = token.payload['user_id']

    accounts = Account.objects.filter(owner=user_id)
    clean_accounts = AccountSerializer(accounts, many=True).data

    categories = Category.objects.filter(owner=user_id)
    clean_categories = CategorySerializer(categories, many=True).data

    transactions = []

    for a in accounts:
        ac = AccountSerializer(a).data
        transaction = Transaction.objects.filter(account=ac['id'])
        clean_transact = TransactionSerializer(transaction, many=True).data
        for t in clean_transact:
            transactions.append(t)

    return Response({"transactions": transactions, "categories": clean_categories, "accounts": clean_accounts})


user_response = openapi.Response('response description', TransactionSerializer)


@swagger_auto_schema(method='post', request_body=TransactionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    transact = TransactionSerializer(data=request.data)

    if transact.is_valid():
        transaction = transact.validated_data
        account = Account.objects.get(id=transaction['account'].id)
        if(transaction['type'] == 'income'):
            balance = account.balance + transaction['amount']
        else:
            balance = account.balance - transaction['amount']
        account.balance = balance
        account.save()
        transact.save()
        # print(transact.validated_data['account'].id)
        return Response(transact.data, status=status.HTTP_201_CREATED)
    return Response(transact.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class CategoryList(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class AccountList(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]


class AccountDetail(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
