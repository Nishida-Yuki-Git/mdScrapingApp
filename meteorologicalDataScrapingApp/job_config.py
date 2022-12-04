import os
from pathlib import Path
from commonUtils.cryptUtils.decrypt import Decrypt

class OnlineBatchSettingClassSingleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

##バッチ基盤用設定クラス
class OnlineBatchSetting(OnlineBatchSettingClassSingleton):
    def __init__(self):
        self.decryptInstance = Decrypt.get_instance()

        ##開発環境用Database設定
        '''
        self.host_id = 'localhost'
        self.port_num = self.decryptInstance.decryptMethod('0CTDx9fP37x8RH8nVFPyNQ==')
        self.db_user = self.decryptInstance.decryptMethod('kuY/GS/nKi760mPD0BcjVA==')
        self.db_password = self.decryptInstance.decryptMethod('Y8PzaXzIQ0JQ8nnrk1RrCQ==')
        self.database_name = self.decryptInstance.decryptMethod('VOhRpoC6ceWlWpXMHb5Rdg==')
        '''

        ##本番環境用Databse設定
        self.host_id = self.decryptInstance.decryptMethod('fRAQORH+jxycZpvuPRgouQ==')
        self.port_num = self.decryptInstance.decryptMethod('0CTDx9fP37x8RH8nVFPyNQ==')
        self.db_user = self.decryptInstance.decryptMethod('UDjr0GudoYMQ+h1gm5QsfQ==')
        self.db_password = self.decryptInstance.decryptMethod('Y8PzaXzIQ0JQ8nnrk1RrCQ==')
        self.database_name = self.decryptInstance.decryptMethod('VOhRpoC6ceWlWpXMHb5Rdg==')

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.MEDIA_URL = '/media/'
        self.MEDIA_ROOT = os.path.join(self.BASE_DIR, 'media')
        self.FILE_SAVE_DIR = '/file/'

        self.smtp_user = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_password = self.decryptInstance.decryptMethod('FZctYTlXWlxWRQh9HVUX5QfoPftJlxRL1LzFIL0M7FQ=')
        self.mail_subject = self.decryptInstance.decryptMethod('Ym8eRw9T4bF7nFa9G+QHwP5OUY4aTOTU01/UM3ytXuSurP3Fe8j94cvRTBQm5H1kISkqKh5yG3AinexERCmHeg==')
        self.mail_body_text = self.decryptInstance.decryptMethod('ok/CrAxlORqCrOQELvhozIqHuIAh5UQUIAkuDyqGqJvrPdpdNv948rgtCuAWR2NEYwvGwLVUpv7zFejIHkN6yBwU2XVQR1Ql9Z2szUxfGAGIAwmHEjzNhtP2fIoVhaFs17oDEwl8WjzShWnqfMvBE2bEB8njQwFk4knMLrppi//SJ/4XBIugsP9d/xZDO0YuUZftwxWnHFfF3I1nIH+2hgwDxykTjq2V7T35/83KqybMeLOQyDjk0QDPRBrHWtWm6CZOCGE3Cj0bClDJ3Qpw24iHsGO+HYlLmTvyuW2koqDzEotVs6g3EubQEiiWhXcoqVQKauROuzrsPHD6y0eX1+jC1LZ93WyLbRi6WJUGFzS+7w7OVvQcUS+gML9tGuR0haIrp2Q0cvQ4TPY/PsKmW7EXbmd6jCC4iYFTn1SUU7XnZPLVTSAbPEdguysqphxVKIJcMosPSM3wWnHQ95WH5oJIe66WotUa11QzPAwX3x1sgRdparMysn44874IXtp9m9tHp6VB7JsmqSS/jtNqmyh4om7umfEnb0hmC/8uwXSvw33IGoNM1SBGKF9q+LY2dGf/4bmwsYfPCQfHkpJk7Ujsm+4wgIbthZbVtGb15Oiu+bE7r8trwzZZCU97V9GJBtftSHlnRk50so3jzXQ2RCggoU3YX+bmnxt/BkO5qS3EJmZmlSosbHA6BrRmz6p+KlUIrxJXQKSqvk2oFa6kSUmiqgKB3CCjfgGY22D4l8SpWii3WzO2ZN/IuNHI6w1uAPJrsoCLns6ttD/fcPuHZUx9m/ZZxAAu0+aA0VqSqViWwAR8TEevmhs1RydeBniUhKHseCkLLzMHFi3DALkm+WVVtxZiqE7RySNsE1fwXOUWmr0C2ffcpkaGAVN8SdCzsWk2buDa+6Zhaq0gqSk97jzQnX68LWqgYGk7NS27mobjb4bD+yKJoA50lXVAZvj9DhhWnzBAEhCeqlCBuQyp0RyEUArU1wCZubHZ5jeLM64=')
        self.mail_from_address = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'
        self.file_dl_url = self.decryptInstance.decryptMethod('oUVkS9X4HmuiLYDQojergPTX+aTAZmDkxkQqkMMP69smLp1a1KgVwh4YgqvQu22F')
        self.sys_url = self.decryptInstance.decryptMethod('oUVkS9X4HmuiLYDQojergPTX+aTAZmDkxkQqkMMP69t10UaP3W+YObE7JO2P84Ko')
        self.mail_sender_name = '気象データ明細出力システム'
        self.mail_sender_encode = 'iso-2022-jp'

    def getHostId(self):
        return self.host_id
    def getPortNum(self):
        return self.port_num
    def getDbUser(self):
        return self.db_user
    def getDbPassWord(self):
        return self.db_password
    def getDatabaseName(self):
        return self.database_name
    def getBaseDir(self):
        return self.BASE_DIR
    def getMediaUrl(self):
        return self.MEDIA_URL
    def getMediaRoot(self):
        return self.MEDIA_ROOT
    def getFileSaveDir(self):
        return self.FILE_SAVE_DIR
    def getSmtpUser(self):
        return self.smtp_user
    def getSmtpPassword(self):
        return self.smtp_password
    def getMailSubject(self):
        return self.mail_subject
    def getMailBodyText(self):
        return self.mail_body_text
    def getMailFromAddress(self):
        return self.mail_from_address
    def getSmtpHost(self):
        return self.smtp_host
    def getSmtpPort(self):
        return self.smtp_port
    def getMailKeisiki(self):
        return self.mail_keisiki
    def getMailCharset(self):
        return self.mail_charset
    def getFileDlUrl(self):
        return self.file_dl_url
    def getSysUrl(self):
        return self.sys_url
    def getMailSenderName(self):
        return self.mail_sender_name
    def getMailSenderEncode(self):
        return self.mail_sender_encode