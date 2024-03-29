from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from presentation.serializer.mdData.userInputItem import *
from presentation.serializer.mdData.mainBusiness import *
from presentation.serializer.mdData.errorRequest import ErrorRequestCommunicater
from presentation.serializer.mdData.fileDownload import FileDownloadCommunicater
import traceback
from presentation.enum.resStatusCode import ResStatusCode
from django.shortcuts import get_object_or_404
from scrapingSystem.models import *


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def UserInputItemView(request):
    """
    画面入力項目設定

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    Response
        HttpResponseオブジェクト
    """

    userid = request.data['userid']
    if request.method == 'POST':
        user_input_item = {
            'user_input_item_list': None,
            'user_process_result': None,
            'status_code': None,
        }
        try:
            get_user_item = UserInputItemCreate(userid)
            user_input_item['user_input_item_list'] = get_user_item['user_input_item_list']
            user_input_item['user_process_result'] = get_user_item['user_process_result']
            user_input_item['status_code'] = ResStatusCode.getSuccessCode()
            return Response(user_input_item)
        except:
            user_input_item['status_code'] = ResStatusCode.getErrorCode()
            return Response(user_input_item)
    return Response(data={'status_code': ResStatusCode.getErrorCode()}, status=400)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@transaction.atomic
def MainBusiness(request):
    """
    メインBL(JSON配列は ‘{“name_filed":["ジャイアン", "スネ夫", "のび太"]}' この形式を想定)

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    Response
        HttpResponseオブジェクト
    """

    userid = request.data['userid']
    if request.method == 'POST':
        user_input_item = {
            'user_input_item_list': None,
            'user_process_result': None,
            'status_code': None,
            'check_message': None,
        }
        try:
            file_create_serializer = FileCreateCommunicater(request)

            check_message = file_create_serializer.checkMainBusinessParam()
            if check_message != None:
                get_user_item = UserInputItemCreate(userid)
                user_input_item['user_input_item_list'] = get_user_item['user_input_item_list']
                user_input_item['user_process_result'] = get_user_item['user_process_result']
                user_input_item['status_code'] = ResStatusCode.getSuccessCode()
                user_input_item['check_message'] = check_message
                return Response(user_input_item)

            file_create_serializer.serveDto()
            get_user_item = UserInputItemCreate(userid)
            user_input_item['user_input_item_list'] = get_user_item['user_input_item_list']
            user_input_item['user_process_result'] = get_user_item['user_process_result']
            user_input_item['status_code'] = ResStatusCode.getSuccessCode()
            return Response(user_input_item)
        except:
            traceback.print_exc()
            user_input_item['status_code'] = ResStatusCode.getErrorCode()
            return Response(user_input_item)
    return Response(data={'status_code': ResStatusCode.getErrorCode()}, status=400)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def ErrorRequest(request):
    """
    エラーファイル作成ビュー

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト

    Returns
    ----------
    Response
        HttpResponseオブジェクト
    """

    if request.method == 'POST':
        user_input_item = {
            'user_input_item_list': None,
            'user_process_result': None,
            'status_code': None,
        }
        try:
            error_request_seria = ErrorRequestCommunicater(request)
            error_request_user_id =  error_request_seria.serveParam()

            get_user_item = UserInputItemCreate(error_request_user_id)
            user_input_item['user_input_item_list'] = get_user_item['user_input_item_list']
            user_input_item['user_process_result'] = get_user_item['user_process_result']
            user_input_item['status_code'] = ResStatusCode.getSuccessCode()
            return Response(user_input_item)
        except:
            traceback.print_exc()
            user_input_item['status_code'] = ResStatusCode.getErrorCode()
            return Response(user_input_item)
    return Response(data={'status_code': ResStatusCode.getErrorCode()}, status=400)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def FileDownload(request, result_file_num):
    """
    ファイルダウンロード

    Parameters
    ----------
    request : HttpRequest
        HttpRequestオブジェクト
    result_file_num : str
        ファイル番号

    Returns
    ----------
    Response
        HttpResponseオブジェクト
    """

    file_download_commu = FileDownloadCommunicater(result_file_num)
    user_file_data = file_download_commu.getFile()

    user_byte_data = {
        'byte_data_list': None,
    }
    user_byte_data['byte_data_list'] = user_file_data
    return Response(user_byte_data)


def UserInputItemCreate(user_id):
    """
    ユーザー用データ作成共通処理

    Parameters
    ----------
    user_id : str
        ユーザーID

    Returns
    ----------
    user_response : dict
        画面表示用ユーザーデータ
    """

    try:
        communicater = UserInputItemCommunicater(user_id)

        year_serializer = YearManageMTSerializer(communicater.getYearManageMTObj(), many=True)
        month_serializer = MonthManageMTSerializer(communicater.getMonthManageMTObj(), many=True)
        ken_serializer = KenParamMTSerializer(communicater.getKenParamMTObj(), many=True)
        md_item_serializer = MDItemMTSerializer(communicater.getMDItemMTObj(), many=True)

        user_result_serializer = ProcessResultDataSerializer(communicater.getProcessResultDataObj(), many=True)

        user_input_item_list = {
            'year_field': year_serializer.data,
            'month_field': month_serializer.data,
            'ken_field': ken_serializer.data,
            'md_item_field': md_item_serializer.data,
        }

        user_process_result = {
            'user_result_field': user_result_serializer.data,
        }

        user_response = {
            'user_input_item_list': user_input_item_list,
            'user_process_result': user_process_result,
        }
        return user_response
    except:
        raise


