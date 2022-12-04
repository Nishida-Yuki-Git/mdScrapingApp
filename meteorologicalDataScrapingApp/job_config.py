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
        self.mail_body_text = self.decryptInstance.decryptMethod('iTw6zYv7JIJsMuod1pqvYYrMZwmmQGHKWLTh+bQhtiB2JcRRKH5lVayr0TSIJf8eg+myACI8BO8DDvAPQcApCe8QIPhsCuURxx5RRx5Y6AbIGWQR5x8n9tUFm8EDwaRr8B5WpekEIZzPkRD+KI7TvRyYdw2nmEennDFN1ucCVPa0Gtp6BIUiOkoMqvtv5tF3bUu7gBq2X780O8U2b0eF/SSGxwjU3vc/d7YvxD+GJeCMLBWgEnfDJt71vu8fNquSUhXW2KhgqJy8kI9XrJv7ypoOQcT1io01sSoyFbtdpcHdPIOtuTMEuhDKUNw6aDsPyE1+H3o1Ca/m03qNK5wwYSh/2AeeSkAgYEdA0lHOkRNPH3q6RdSF/SnA6S4NzzSaQ27jrMGAETKV7DnbTl1eCoLVYrVLoSGhiUYb6qzTOxcEMuymC0mBm9zQTjl3ktb89gqTL6JmyYIgfzYIY86dyBcD9quYPhVSh9QZCGKa8DbpGkBlp6EHbl2ktdb7SQItLt50KQy/g4q6VTrEYXFuUm3WojBACv7Z1Acs2w1HwNlVaCysl2j+U4Tbff2psD/fsgKbgUtOnuUIvhbDYKXbaHaL1lG3ISM7QvuVanIYjYMFyqICset6tpeypfnKd5ZyhyD6dyX/ZkMH7bGM4pda87ebc0CPBlpEbFd56qzK3bGsUgA3k9JaBHVKhbNbu9n9V+92VNfwS8EwcsjZbym3Xi9ZG5V940s3lJ2LgoKuetRHuAQXu51tsvXXKH5l83Ru+xYryE3tQZYFGgKcW80B7SGKPtAojU9o4ulS+cFBVGj42bJlOfna8EtNThe5j3IvyDyFv0uXzhq+a0iXqtuVRh57aBbodooV5qHN9aHYs2JNasAK1vcF+WGzGswsguPubMKk5AyTMpZuvtwTWo8c1KtKXpk9yIrfvHekbaVwqasoZq1Q5IYdRLMN1OV3Z9lDpI5WfqQNsjqd1y5Nzmhohhby1CaP1zfu8b2x79fRCGo=')
        self.mail_from_address = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'
        self.file_dl_url = self.decryptInstance.decryptMethod('uaLQAmLm6UhX7/HS4sD9OnyiP6FKUrNN9Ozlku1EtjF7NYC8VXbtg+3bngQdnxN3ZdkMT2J4Ba/hyF+Ain6g0Q==')
        self.sys_url = self.decryptInstance.decryptMethod('uaLQAmLm6UhX7/HS4sD9OnyiP6FKUrNN9Ozlku1EtjHv/Gy6EHjrc37Q163N2l5J')
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