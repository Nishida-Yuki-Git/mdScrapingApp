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
import shutil
from django.http import HttpResponse
import mimetypes

##画面入力項目設定
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def UserInputItemView(request):
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


##メインBL(JSON配列は ‘{“name_filed":["ジャイアン", "スネ夫", "のび太"]}' この形式を想定)
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@transaction.atomic
def MainBusiness(request):
    userid = request.data['userid']
    if request.method == 'POST':
        user_input_item = {
            'user_input_item_list': None,
            'user_process_result': None,
            'status_code': None,
        }
        try:
            file_create_serializer = FileCreateCommunicater(request)
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


##エラーファイル作成ビュー
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def ErrorRequest(request):
    userid = request.data['userid']
    if request.method == 'POST':
        user_input_item = {
            'user_input_item_list': None,
            'user_process_result': None,
            'status_code': None,
        }
        try:
            error_request_seria = ErrorRequestCommunicater(request)
            error_request_seria.serveParam()
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


##ファイルダウンロード
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def FileDownload(request):
    if request.method == 'POST':
        user_item = {
            'file_response': None,
            'status_code': None,
        }
        try:
            file_download_seria = FileDownloadCommunicater(request)
            file_obj = file_download_seria.getFile()

            file = file_obj['file']
            name = file_obj['name']
            response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={name}'
            shutil.copyfileobj(file, response)
            print(file)
            print(name)
            print(type(file))
            print(type(name))
            print(response)

            user_item['file_response'] = response
            user_item['status_code'] = ResStatusCode.getSuccessCode()
            return Response(user_item)
        except:
            traceback.print_exc()
            user_item['status_code'] = ResStatusCode.getSuccessCode()
            return Response(user_item)
    return Response(data={'status_code': ResStatusCode.getErrorCode()}, status=400)


##ユーザー用データ作成共通処理
def UserInputItemCreate(user_id):
    try:
        communicater = UserInputItemCommunicater(user_id)

        year_serializer = YearManageMTSerializer(communicater.getYearManageMTObj(), many=True)
        month_serializer = MonthManageMTSerializer(communicater.getMonthManageMTObj(), many=True)
        ken_serializer = KenParamMTSerializer(communicater.getKenParamMTObj(), many=True)
        md_item_serializer = MDItemMTSerializer(communicater.getMDItemMTObj(), many=True)

        user_result_serializer = ProcessResultDataSerializer(communicater.getProcessResultDataObj(), many=True)

        ##ユーザー入力項目
        user_input_item_list = {
            'year_field': year_serializer.data,
            'month_field': month_serializer.data,
            'ken_field': ken_serializer.data,
            'md_item_field': md_item_serializer.data,
        }

        ##ユーザー処理結果
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


