# Generated by Django 3.2.8 on 2021-12-14 12:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userid', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='userid')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('profile', models.CharField(blank=True, max_length=255, verbose_name='profile')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
        migrations.CreateModel(
            name='FileManageData',
            fields=[
                ('result_file_num', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('create_file', models.FileField(max_length=500, upload_to='file')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralCodeMT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_group_key', models.CharField(max_length=8)),
                ('general_key', models.CharField(max_length=8)),
                ('general_code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='JobParamData',
            fields=[
                ('job_num', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('job_start_year', models.CharField(max_length=5)),
                ('job_end_year', models.CharField(max_length=5)),
                ('job_start_month', models.CharField(max_length=3)),
                ('job_end_month', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='JobParamDetailData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_num', models.CharField(max_length=13)),
                ('job_item_id', models.IntegerField()),
                ('job_ken', models.CharField(max_length=5)),
                ('job_md_item', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='JobQueData',
            fields=[
                ('job_num', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('result_file_num', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='KenParamMT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ken_name', models.CharField(max_length=5)),
                ('ken_no', models.IntegerField()),
                ('ken_block_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MDItemMT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md_item', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MdUrlMT',
            fields=[
                ('md_url_seq', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('md_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MonthManageMT',
            fields=[
                ('month_param', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessResultData',
            fields=[
                ('result_file_num', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=10)),
                ('file_create_status', models.CharField(max_length=20)),
                ('create_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('target_start_year', models.CharField(max_length=5)),
                ('target_end_year', models.CharField(max_length=5)),
                ('target_start_month', models.CharField(max_length=3)),
                ('target_end_month', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessResultDetailData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_file_num', models.CharField(max_length=20)),
                ('result_item_id', models.IntegerField()),
                ('target_ken', models.CharField(max_length=5)),
                ('target_md_item', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='SaibanMT',
            fields=[
                ('saiban_key', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('saiban_count', models.IntegerField()),
                ('saiban_ketasu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskManageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=4)),
                ('user_id', models.CharField(max_length=10)),
                ('task_process_flag', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='YearManageMT',
            fields=[
                ('year_param', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddConstraint(
            model_name='taskmanagedata',
            constraint=models.UniqueConstraint(fields=('task_id', 'user_id'), name='unique_task_manage'),
        ),
        migrations.AddConstraint(
            model_name='processresultdetaildata',
            constraint=models.UniqueConstraint(fields=('result_file_num', 'result_item_id'), name='unique_user_result'),
        ),
        migrations.AddConstraint(
            model_name='jobparamdetaildata',
            constraint=models.UniqueConstraint(fields=('job_num', 'job_item_id'), name='unique_job_param'),
        ),
        migrations.AddConstraint(
            model_name='generalcodemt',
            constraint=models.UniqueConstraint(fields=('general_group_key', 'general_key'), name='unique_general_code'),
        ),
    ]
