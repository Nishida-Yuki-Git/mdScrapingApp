import os
from pathlib import Path
from commonUtils.cryptUtils.decrypt import Decrypt

##バッチ基盤用設定クラス
class OnlineBatchSetting():
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
        self.mail_subject = self.decryptInstance.decryptMethod('J6VqQH+NtszZTBcpBYxEfRfLC8X45M9nHH4+EA2RU9fiaW99hXOwG1TraauYjv5g+77yTt+irN0/j+2CxKuJhw==')
        self.mail_body_text = self.decryptInstance.decryptMethod('c4mo6pbL7j25W6Jg5ETPVTd1Qm9bLfiwiT4lfITxbwsw7qK6zRKy1Ah1YgdqeNfCo5/prkh8JLXrhQEmTsJjTXYCkg6brcAjhCt/hn2fknBH9Ien0sQFhisY8hdwcE8u216QIKl2BtFla5/NRHXWRlIZTpxgVLNp4gEuLaAFA68/7kK6+jM9VCfXv/pnrqmrZPF6AgX0KblBWHMf7sPpBhaKvrVX+JeTtWu7Kw0YIENKY+QTsEzonxv75vUWXyA/USP6B72S8iN9b0ywVaE6mbJUN1AC7BK3R4Y2X12RtV+qdtQ4Ae7/tgDZNexY4keUFPphY/w1df+sh8vDZep0mHNuIEyTdPLQ03CkRC039Rep3T9ZkHgj4BaAcH7GOY5SRkXgdlnvzclP6iVOwqf6rbcfzHniVEn2XyQ5jsa0uHJm9j6/gqAYDgY8TlKei7XylulDWH3NIdeGNxzVAlF6mYHhoVU42TR80ae0MexbZOttPBvg6YtfkPycJ6+M+xbYBn0FE0qvoxvZ5UKRjVnyuvoyr2WeICk+cQpbWvFyRzdaSx0Q1g/O2UWwU/FK9mAQu7jJYv6uk4yfhJ46jHZvczfRY+ZCPBYO+XsyFmM6hLoXprrqyAfRKJoczXeus+K5CdlFV2iDgBMyWBiUaKFtbDJLTFNnYdxScnGgmAXZnARmo21iUDr/OIGfIpU2BBKNJWg1MUMSq0/tvsmwaYVubV/5lFVe6nC8lFTRs2NLunLkFdYaZrP7O+QlVefC0ixYh5vVPuZzM8y0LPi81jyfWF3vjDVPvgS+YyREroksZXjCN+euK4kBTu4jTgbd0ksC8E6UyYgKcgymg1bk4U/tyUnHp5kBOWfJ5QpqwtUzVY6RuARZj+a9Wj9fdPIgYOeMPYKzlKKWl7S9a91A6vvN/4YKoh12k7lFyFwMxT24+KTCNYdF/4/ijMJwV0MlQSpFrayUVanTs50wGQYGessMyNxYevsS1IihhmUdTmQPPrALKgrY8qd/R6if7r+DoJgO')
        self.mail_from_address = self.decryptInstance.decryptMethod('5P93ybuHj4RdWZJLf/WdnPPgkf1pL5MB1Ky9Dw6UXSc=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'
        self.file_dl_url = self.decryptInstance.decryptMethod('poH1WtpbzBTofiY85B+J9VGr+42Yw7+pmWC5tayiTQyCHJe/fmyFNGp0W5vuB0MZ')
        self.sys_url = self.decryptInstance.decryptMethod('poH1WtpbzBTofiY85B+J9VGr+42Yw7+pmWC5tayiTQyoSlWj/0o5L7w+mVJAFFVO')

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