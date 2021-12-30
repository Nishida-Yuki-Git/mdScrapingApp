from rest_framework import generics, permissions, status
from rest_framework.response import Response
from presentation.serializer.account.account import AccountSerializer
from django.db import transaction

#ユーザー作成(POST)
class AuthRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AccountSerializer

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ユーザ情報取得のView(GET)
class AuthInfoGetView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request, format=None):
        return Response(data={
            'userid': request.user.userid,
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
            },
            status=status.HTTP_200_OK)

##認証確認用ビュー(メインBL起動前に毎回ここで確認させる)
class AuthenticationCheckView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        return Response("認証OKです", status=status.HTTP_200_OK)

