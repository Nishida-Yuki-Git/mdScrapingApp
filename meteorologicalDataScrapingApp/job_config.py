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
        self.mail_body_text = self.decryptInstance.decryptMethod('c4mo6pbL7j25W6Jg5ETPVTd1Qm9bLfiwiT4lfITxbwsw7qK6zRKy1Ah1YgdqeNfCo5/prkh8JLXrhQEmTsJjTXYCkg6brcAjhCt/hn2fknBH9Ien0sQFhisY8hdwcE8u216QIKl2BtFla5/NRHXWRlIZTpxgVLNp4gEuLaAFA68/7kK6+jM9VCfXv/pnrqmrZPF6AgX0KblBWHMf7sPpBhaKvrVX+JeTtWu7Kw0YIENKY+QTsEzonxv75vUWXyA/USP6B72S8iN9b0ywVaE6mbJUN1AC7BK3R4Y2X12RtV+qdtQ4Ae7/tgDZNexY4keUFPphY/w1df+sh8vDZep0mHNuIEyTdPLQ03CkRC039Rep3T9ZkHgj4BaAcH7GOY5SRkXgdlnvzclP6iVOwqf6rdmGpxu6mc9PW+LP62Nko178sHn1cSblrJeTjG1Ygd3qME4BkY5+GoQ2YcZENygCo4GfpmBhMPhA1/8fmXgiWk8Uci5ZoYh297kEcnxLet53I0/WfvtDuYApjxnHF2eLUxrlznWzUxZOsfVRcU2iJ3qrY6VMMIqorKdRjsDhaNQAsUzhAMXdi7nTgarMMzK8sgJs0Efr90EiN23kqSaqekucoyzHxm1k4ZIltr5lBr/y+5v3NZHbqp+lPVbbT4KNVSdYlmlZa2lc4r4ZfiO0U56d6d/Y5EQMGt+g/o14AA3SDsAVkGst6fowkS4zyLjNn73VcNEinDWAchbgbCAt24RE5VKuU2HhEWci+gMADHowHP+MX+BbzwkgISDaJCBFsXteW+3M6jKmqQ3P5Dwg7t1DsyU5xKBQdlhjQhPl/KZW9FdeVKLCKefwEqAIXvrOwGSDMK3rEwj4XTMxxj1HgmmowQ7tFL3Akz9CSDPRSzDVQNPXmkexS3/Fsp7mgM9viSXe3zaEpLQelTxCl++3IiXeCTgfx+6/yYdNG63CmiX+')
        self.mail_from_address = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'
        self.file_dl_url = self.decryptInstance.decryptMethod('poH1WtpbzBTofiY85B+J9VGr+42Yw7+pmWC5tayiTQyCHJe/fmyFNGp0W5vuB0MZ')
        self.sys_url = self.decryptInstance.decryptMethod('poH1WtpbzBTofiY85B+J9VGr+42Yw7+pmWC5tayiTQyoSlWj/0o5L7w+mVJAFFVO')
        self.mail_sender_name = '[MD-SYS]気象データ収集システム'
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