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
        self.mail_body_text = self.decryptInstance.decryptMethod('Oc0SJ84BorL4IFaADuRquyq77I3/dALFfXzAuPnfhC0+3SKPQ3mJ+A+cYu+P/+JEfbrqqnhBbH1htyhzgWmz9tPdYaBCcmkVVDps04/WA+C9ak33CIKv5Qwf4T5oaOjdI4+7257kUeg1+xM6mEYTnqbd+po1W6hlel4Fay9vRRbjqzi19XE1Z3zUYBR7AnXmOYlu4bwUECVaRz5wUnrOUFWPD+CNOfNE7lgu7u+rZ8WQM9YKh5D6c61CW8R7z2Xqd7zN+x8PmAD6S5vPYJYbS1NBn2OZMHy6moeUkkQhIGbTICbrpRFw/P6qwtfEhBkW8KQt8nhno9zZW5T2fkEA8ZfcMaw+ZNeOz8ZsAGJG1+1NfRWAf1Z5eDzED/e80ulk6LNJcVVPCb0Qk4Ycq94u3GLmC3kx1NMr1RYuyIWEg/S3OjDdbjysVp/PlBWiUKYTcJv7Wr1qicDjF4zFPUGE/OujSDJySq+h0QrcQWTUYoFwhsCog+VcpjtUP8gm1bqn3GMtyn8J8cDYuvRXMPCGPzSBgz2ihGOcy3XyhWGxZG5YrwsiZ1jze4bvsB/XUZmAm3mboJbq0hbJVRJ4v2RkuG7bOw//Djv8mcth7LdwL3PBzZ6qIZSvInyedJdFxaJh0Nby+Hf9/QoPTTvthgJnKqqbTpD/sIYMe2RNgND9B0WBLqP0nQDwzx14B2C13RoQpp1tELhETjU96nK4V8++A1URUA371TmEq3yE9noSYPV+E4Uaq5F8C0vrK6Ychscypl78PcuqZRfNWAZSXmxNw7mDW0cWhNXbAq+Au/irPRAyb4KwVILRQulMLxBxrEO1XxL4IpZqMUNYYC2/Tg7mf3b4E4fUCivY6P9qCreh0LKmXxFDrSPEgOANktLbPR2kElhQ2tggdcqoQqGUa+ol/Op/zKxJ0Slw7AWifGXMS64=')
        self.mail_from_address = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'
        self.file_dl_url = self.decryptInstance.decryptMethod('oUVkS9X4HmuiLYDQojergPTX+aTAZmDkxkQqkMMP69smLp1a1KgVwh4YgqvQu22F')
        self.sys_url = self.decryptInstance.decryptMethod('oUVkS9X4HmuiLYDQojergPTX+aTAZmDkxkQqkMMP69tu/otLlZIhIUfn0Eo0PSti')
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