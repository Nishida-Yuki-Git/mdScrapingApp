from django.db import models
from django.utils import timezone

##県パラメータマスタ
class KenParamMT(models.Model):
    ken_name = models.CharField(max_length=5)
    ken_no = models.IntegerField()
    ken_block_no = models.IntegerField()
    def __str__(self):
        return self.ken_name

##「気象庁」URL部品マスタ
class MdUrlMT(models.Model):
    md_url = models.CharField(max_length=200)
    def __str__(self):
        return self.md_url

##気象データ項目マスタ
class MDItemMT(models.Model):
    md_item = models.CharField(max_length=10)
    def __str__(self):
        return self.md_item

##ユーザーデータ
class UserData(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    user_name = models.CharField(max_length=20)
    mail_address = models.EmailField( max_length=254)
    pass_word = models.CharField(max_length=10)
    def __str__(self):
        return self.user_id

##ジョブキューデータ
class JobQueData(models.Model):
    job_num = models.CharField(max_length=13, primary_key=True)
    user_id = models.CharField(max_length=10)
    result_file_num = models.CharField(max_length=20)
    def __str__(self):
        return self.job_num

##ジョブパラメータデータ(今の仕様での暫定レイアウト:本番は,1項目1値とは限らないので、項目IDもPKとして追加したほうがいい)
class JobParamData(models.Model):
    job_num = models.CharField(max_length=13)
    param_name = models.CharField(max_length=20)
    param = models.CharField(max_length=30)
    def __str__(self):
        return self.job_num + '/' + self.param_name + '/' + self.param
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['job_num', 'param_name'], name='unique_job')
       ]

##採番管理マスタ
class SaibanMT(models.Model):
    saiban_key = models.CharField(max_length=10, primary_key=True)
    saiban_count = models.IntegerField()
    saiban_ketasu = models.IntegerField()
    def __str__(self):
        return self.saiban_key + '/' + str(self.saiban_count) + '/' + str(self.saiban_ketasu)

##処理結果データ
class ProcessResultData(models.Model):
    result_file_num = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=10)
    file_create_status = models.CharField(max_length=20)
    create_date_time = models.DateTimeField(default=timezone.now)
    target_start_year = models.CharField(max_length=5)
    target_end_year = models.CharField(max_length=5)
    target_start_month = models.CharField(max_length=3)
    target_end_month = models.CharField(max_length=3)
    target_ken = models.CharField(max_length=5)
    target_md_item = models.CharField(max_length=5)
    def __str__(self):
        return self.result_file_num+'/'+self.user_id

##物理ファイル管理データ
class FileManageData(models.Model):
    result_file_num = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=10)
    create_file = models.FileField(upload_to='file', max_length=500)
    def __str__(self):
        return self.result_file_num

##汎用マスタ
class GeneralCodeMT(models.Model):
    general_group_key = models.CharField(max_length=8)
    general_key = models.CharField(max_length=8)
    general_code = models.CharField(max_length=50)
    def __str__(self):
        return self.general_group_key+'/'+self.general_key+'/'+self.general_code
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['general_group_key', 'general_key'], name='unique_general_code')
       ]

##タスク管理マスタ
'''(これは臨時で処理に対応するためのマスタテーブルです)
task_id -> 0001：気象データ収集
task_process_flag -> 0：待機中, 1：実行中
'''
class TaskManageMt(models.Model):
    task_id = models.CharField(max_length=4, primary_key=True)
    task_process_flag = models.CharField(max_length=1)
    def __str__(self):
        return self.task_id+'/'+self.task_process_flag
















