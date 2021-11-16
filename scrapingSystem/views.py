from django.shortcuts import render
from scrapingSystem.SaibanService import SaibanService
from django.conf import settings
import datetime
from django.views.generic import CreateView
from .models import *
from django.views import View
from django.shortcuts import get_object_or_404
import mimetypes
from django.http import HttpResponse
import shutil
from scrapingSystem.taskManage import mdScrapingTask
import threading

#アカウント作成
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        user_id_post = request.POST['user_id']
        user_name_post = request.POST['user_name']
        user_mail_address_post = request.POST['mail_address']
        user_pass_word_post = request.POST['pass_word']

        ##DBに登録
        user_data = UserData(
            user_id=user_id_post,
            user_name=user_name_post,
            mail_address=user_mail_address_post,
            pass_word=user_pass_word_post)
        user_data.save()

        ##セッションに保存
        request.session['session_user_id'] = user_id_post;

        ##共通入力項目の取得
        user_parts = userFormset()
        user_parts['login_user_id'] = request.session['session_user_id']
        return render(request, 'scrapingSystem/index.html', {'user_parts' : user_parts})

    def get(self, request, *args, **kwargs):
        return  render(request, 'scrapingSystem/create.html')

create_account = Create_account.as_view()

#ログイン機能
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        ##ログイン処理
        user_data = UserData.objects.get(pk=request.POST['user_id'])
        if user_data == None:
            return render(request, 'scrapingSystem/login.html')
        elif user_data.pass_word != request.POST['pass_word']:
            return render(request, 'scrapingSystem/login.html')
        else:
            ##セッションに保存
            request.session['session_user_id'] = request.POST['user_id']
            ##共通入力項目の取得
            user_parts = userFormset()
            user_parts['login_user_id'] = request.session['session_user_id']
            return render(request, 'scrapingSystem/index.html', {'user_parts' : user_parts})

    def get(self, request, *args, **kwargs):
        return render(request, 'scrapingSystem/login.html')

account_login = Account_login.as_view()

##ログアウト
def account_logout(request):
    ##セッションの破棄
    request.session.clear()

    ##共通入力項目の取得
    user_parts = userFormset()
    user_parts['login_user_id'] = 'null_user'
    return render(request, 'scrapingSystem/index.html', {'user_parts' : user_parts})

def IndexView(request):
    ##共通入力項目の取得
    user_parts = userFormset()
    try:
        login_user_id = request.session['session_user_id']
        login_user_result_obj = ProcessResultData.objects.filter(
            user_id = request.session['session_user_id'])
        login_user_file = FileManageData.objects.filter(
            user_id = request.session['session_user_id'])

        user_result_list = []
        user_parts['login_user_id'] = login_user_id
        for (user_result, user_file) in zip(login_user_result_obj, login_user_file):
            user_result_list.append({
                'user_result' : user_result,
                'user_file' : user_file
            })

        user_parts['login_user_id'] = login_user_id
        user_parts['user_result_list'] = user_result_list
    except:
        user_parts['login_user_id'] = 'null_user'
        user_parts['user_result_list'] = 'null_result'

    return render(request, 'scrapingSystem/index.html', {'user_parts' : user_parts})


def results(request):
    ##POSTデータの受け取り
    select_start_year = request.POST['start-year-select']
    select_end_year = request.POST['end-year-select']
    select_start_month = request.POST['start-month-select']
    select_end_month = request.POST['end-month-select']
    select_ken = request.POST['ken-select']
    select_md_item = request.POST['md-item-select']

    ##POSTデータのリスト化
    post_name_list = []
    post_data_list = []
    post_name_list.append('select_start_year')
    post_name_list.append('select_end_year')
    post_name_list.append('select_start_month')
    post_name_list.append('select_end_month')
    post_name_list.append('select_ken')
    post_name_list.append('select_md_item')
    post_data_list.append(select_start_year)
    post_data_list.append(select_end_year)
    post_data_list.append(select_start_month)
    post_data_list.append(select_end_month)
    post_data_list.append(select_ken)
    post_data_list.append(select_md_item)

    ##採番サービスでジョブIDを採番する
    saiban_key = 'jobKey'
    saiban_service = SaibanService.SaibanService(saiban_key)
    saiban_job_num = saiban_service.saibanMethod()

    ##処理結果ファイル番号の採番
    file_num_date_time = (datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    ##処理結果の初期ステータスを取得
    first_status_obj = GeneralCodeMT.objects.get(
        general_group_key = 'GR000001',
        general_key = '01')
    first_status = first_status_obj.general_code

    ##ジョブ登録
    user_job_data = JobQueData(
        job_num=saiban_job_num,
        user_id=request.session['session_user_id'],
        result_file_num=file_num_date_time)
    user_job_data.save()
    for i in range(len(post_data_list)):
        user_job_param_data = JobParamData(
            job_num=saiban_job_num,
            param_name=post_name_list[i],
            param=post_data_list[i])
        user_job_param_data.save()

    ##ログインユーザーの処理結果データに追加登録
    user_process_status = ProcessResultData(
        result_file_num=file_num_date_time,
        user_id=request.session['session_user_id'],
        file_create_status=first_status,
        target_start_year=select_start_year,
        target_end_year=select_end_year,
        target_start_month=select_start_month,
        target_end_month=select_end_month,
        target_ken=select_ken,
        target_md_item=select_md_item)
    user_process_status.save()

    ##物理ファイル保管テーブルにファイル番号とユーザーIDを登録
    user_file_manage_obj = FileManageData(
        result_file_num=file_num_date_time,
        user_id=request.session['session_user_id'])
    user_file_manage_obj.save()

    ##データ収集バッチの起動
    thread = threading.Thread(target=mdScrapingTask.goFlow)
    thread.start()

    ##共通入力項目の取得
    user_parts = userFormset()
    try:
        login_user_id = request.session['session_user_id']
        login_user_result_obj = ProcessResultData.objects.filter(
            user_id = request.session['session_user_id'])
        login_user_file = FileManageData.objects.filter(
            user_id = request.session['session_user_id'])

        user_result_list = []
        user_parts['login_user_id'] = login_user_id
        for (user_result, user_file) in zip(login_user_result_obj, login_user_file):
            user_result_list.append({
                'user_result' : user_result,
                'user_file' : user_file
            })

        user_parts['login_user_id'] = login_user_id
        user_parts['user_result_list'] = user_result_list

    except:
        user_parts['login_user_id'] = 'null_user'
        user_parts['user_result_list'] = 'null_result'

    return render(request, 'scrapingSystem/index.html', {'user_parts': user_parts})

def download(request, result_file_num):
    user_file = get_object_or_404(FileManageData, result_file_num=result_file_num)
    file = user_file.create_file
    name = file.name

    response = HttpResponse(content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={name}'
    shutil.copyfileobj(file, response)

    return response

##Form項目の設定共通部品
def userFormset():
    ##設定ファイルから読み込み
    start_year = getattr(settings, "START_YEAR", None)
    one_year_month_list = getattr(settings, "YEAR_MONTH", None)

    ##年リスト
    MD_year_list = []
    today = datetime.date.today()
    for i in range(start_year, today.year):
        MD_year_list.append(i)

    ##マスタから「県」と「気象データ項目」を取得
    ken_list = KenParamMT.objects.all()
    md_item_list = MDItemMT.objects.all()

    user_form_parts = {
        'one_year_month_list' : one_year_month_list,
        'MD_year_list' : MD_year_list,
        'ken_list' : ken_list,
        'md_item_list' : md_item_list
    }
    return user_form_parts



