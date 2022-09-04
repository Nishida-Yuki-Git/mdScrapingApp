from rest_framework import generics, permissions, status
from rest_framework.response import Response
from presentation.serializer.account.account import AccountSerializer
from django.db import transaction
import traceback
from presentation.enum.resStatusCode import ResStatusCode


class AuthRegister(generics.CreateAPIView):
    """ ユーザー作成(POST)
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = AccountSerializer

    @transaction.atomic
    def post(self, request, format=None):
        """
        ユーザーアカウント作成を実行する

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト
        format : str

        Returns
        ----------
        Response
            HttpResponseオブジェクト
        """

        front_res = {
            'serializer_data': None,
            'status_code': None
        }
        try:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                front_res['serializer_data'] = serializer.data
                front_res['status_code'] = ResStatusCode.getSuccessCode()
                return Response(front_res, status=status.HTTP_201_CREATED)

            front_res['serializer_data'] = serializer.errors
            front_res['status_code'] = ResStatusCode.getErrorCode()
            return Response(front_res, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            front_res['status_code'] = ResStatusCode.getErrorCode()
            return Response(front_res, status=500)


class AuthInfoGetView(generics.RetrieveAPIView):
    """ ユーザ情報取得のView(GET)
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request, format=None):
        """
        ユーザー情報を取得する

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト
        format : str

        Returns
        ----------
        Response
            HttpResponseオブジェクト
        """

        return Response(data={
            'userid': request.user.userid,
            'username': request.user.username,
            'email': request.user.email,
            'profile': request.user.profile,
            'status_code': ResStatusCode.getSuccessCode()
            },
            status=status.HTTP_200_OK)


class AuthenticationCheckView(generics.RetrieveAPIView):
    """ 認証確認用ビュー
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        認証確認用を実行する(メインBL起動前に毎回ここで確認させる)

        Parameters
        ----------
        request : HttpRequest
            HttpRequestオブジェクト
        format : str

        Returns
        ----------
        Response
            HttpResponseオブジェクト
        """

        front_res = {
            'status_code': ResStatusCode.getSuccessCode()
        }
        return Response(front_res, status=status.HTTP_200_OK)

