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

        self.smtp_user = self.decryptInstance.decryptMethod('Zli7+HnE5TRUefjAIA4nHaTS//qQxfPs7FZpfXKhIOI=')
        self.smtp_password = self.decryptInstance.decryptMethod('SuaBig3cDjUfNyWd8zSOaP2T5k1v66fyTT1uLc/73ro=')
        self.mail_subject = self.decryptInstance.decryptMethod('Q9FBFq0lTc5UgKMxDwVEVy9PEq3fx2WHDs8i54ASXMJX0kxMxyQeW/vkymPDjjgZzayC9Vbf92lYAzEn4E2IRQ==')
        self.mail_body_text = self.decryptInstance.decryptMethod('Sdnve6s6IlI1PsI6fJXAfvA+j8w8+7m/Z3yudvpaYetLPcL9Qs6Duu+NUOULNZ1HIzCXWmzJ7iczt7XJ7EP45ztDrk1xzxt4TkpLD/ZorMmVyPgLpN+1OPzpP5ZEwxQ0')
        self.mail_from_address = self.decryptInstance.decryptMethod('Zli7+HnE5TRUefjAIA4nHaTS//qQxfPs7FZpfXKhIOI=')
        self.smtp_host = self.decryptInstance.decryptMethod('LEkQtfN2LfBGVtIv6GEvbg==')
        self.smtp_port = int(self.decryptInstance.decryptMethod('LF0biTzquluSHz4s16HAzQ=='))
        self.mail_keisiki = 'plain'
        self.mail_charset = 'utf-8'

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