from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, _user_has_perm
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

##データ収集可能範囲年管理用マスタ
class YearManageMT(models.Model):
    year_param = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.year_param

##「月」管理用マスタ
class MonthManageMT(models.Model):
    month_param = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.month_param

##県パラメータマスタ
class KenParamMT(models.Model):
    ken_name = models.CharField(max_length=5)
    ken_no = models.IntegerField()
    ken_block_no = models.IntegerField()
    def __str__(self):
        return self.ken_name

##「気象庁」URL部品マスタ
class MdUrlMT(models.Model):
    md_url_seq = models.CharField(max_length=1, primary_key=True)
    md_url = models.CharField(max_length=200)
    def __str__(self):
        return self.md_url_seq + '/' + self.md_url

##気象データ項目マスタ
class MDItemMT(models.Model):
    md_item = models.CharField(max_length=100)
    def __str__(self):
        return self.md_item


##ユーザーデータ
class AccountManager(BaseUserManager):
    def create_user(self, request_data, **kwargs):
        now = timezone.now()
        if not request_data['email']:
            raise ValueError('Users must have an email address.')

        profile = ""
        if request_data.get('profile'):
            profile = request_data['profile']

        user = self.model(
            userid=request_data['userid'],
            username=request_data['username'],
            email=self.normalize_email(request_data['email']),
            is_active=True,
            last_login=now,
            date_joined=now,
            profile=profile
        )

        user.set_password(request_data['password'])
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        request_data = {
            'userid': 'yuki01',
            'username': username,
            'email': email,
            'password': password
        }
        user = self.create_user(request_data)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    userid = models.CharField(_('userid'), max_length=10, primary_key=True, unique=True)
    username    = models.CharField(_('username'), max_length=30, unique=True)
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    profile     = models.CharField(_('profile'), max_length=255, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def user_has_perm(self, user, perm, obj):
        return _user_has_perm(self, user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        swappable = 'AUTH_USER_MODEL'


##ジョブキューデータ
class JobQueData(models.Model):
    job_num = models.CharField(max_length=13, primary_key=True)
    user_id = models.CharField(max_length=10)
    result_file_num = models.CharField(max_length=20)
    def __str__(self):
        return self.job_num

##ジョブパラメータデータ
class JobParamData(models.Model):
    job_num = models.CharField(max_length=13, primary_key=True)
    job_start_year = models.CharField(max_length=5)
    job_end_year = models.CharField(max_length=5)
    job_start_month = models.CharField(max_length=3)
    job_end_month = models.CharField(max_length=3)
    def __str__(self):
        return self.job_num

##ジョブパラメータ明細データ
class JobParamDetailData(models.Model):
    job_num = models.CharField(max_length=13)
    job_item_id = models.IntegerField()
    job_ken = models.CharField(max_length=5, blank=True)
    job_md_item = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.job_num+'/'+self.job_item_id
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['job_num', 'job_item_id'], name='unique_job_param')
        ]

##採番管理マスタ
class SaibanMT(models.Model):
    saiban_key = models.CharField(max_length=10, primary_key=True)
    saiban_count = models.IntegerField()
    saiban_ketasu = models.IntegerField()
    def __str__(self):
        return self.saiban_key + '/' + str(self.saiban_count) + '/' + str(self.saiban_ketasu)

##ユーザー処理結果データ
class ProcessResultData(models.Model):
    result_file_num = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=10)
    file_create_status = models.CharField(max_length=20)
    create_date_time = models.DateTimeField(default=timezone.now)
    target_start_year = models.CharField(max_length=5)
    target_end_year = models.CharField(max_length=5)
    target_start_month = models.CharField(max_length=3)
    target_end_month = models.CharField(max_length=3)
    def __str__(self):
        return self.result_file_num+'/'+self.user_id

##ユーザー処理結果明細データ
class ProcessResultDetailData(models.Model):
    result_file_num = models.CharField(max_length=20)
    result_item_id = models.IntegerField()
    target_ken = models.CharField(max_length=5, blank=True)
    target_md_item = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.result_file_num+'/'+str(self.result_item_id)
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['result_file_num', 'result_item_id'], name='unique_user_result')
        ]

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

##タスク管理データ
'''
task_id -> 0001：新規ファイル作成, 0002：エラーファイル作成
'''
class TaskManageData(models.Model):
    task_id = models.CharField(max_length=4)
    user_id = models.CharField(max_length=10)
    task_thread_num = models.CharField(max_length=1)
    def __str__(self):
        return self.task_id+'/'+self.user_id+'/'+self.task_thread_num
    class Meta:
        constraints = [
           models.UniqueConstraint(fields=['task_id', 'user_id'], name='unique_task_manage')
        ]
