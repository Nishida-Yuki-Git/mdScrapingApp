from mainJobBatch.taskManage.serviceBase.mdScrapingMailService import MdScrapingMailService
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
from mainJobBatch.taskManage.dao.mailSendDao import MailSendDao
from mainJobBatch.taskManage.dao.daoImple.mailSendDaoImple import MailSendDaoImple
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from mainJobBatch.taskManage.exception.mdException import MdException

class MdScrapingMailServiceImpl(MdScrapingMailService):
    """
    気象データ収集メール送信サービス基底実装クラス

    Attributes
    ----------
    batch_setting : OnlineBatchSetting
        バッチ設定ファイル
    smtp_user : str
        SMTPサーバーログインユーザー
    smtp_password : str
        SMTPサーバーパスワード
    mail_subject : str
        メール件名
    mail_body_text : str
        メール本文
    mail_from_address : str
        メール送信元アドレス
    smtp_host : str
        SMTPサーバーホストアドレス
    smtp_port : str
        SMTPサーバーポート番号
    mail_keisiki : str
        メール形式
    mail_charset : str
        メール送信時文字コード
    file_dl_url : str
        ファイルダウンロード用システムURL
    sys_url : str
        システムURL
    content_disc : str
        content_discコンスト文字列
    attachment : str
        attachmentコンスト文字列
    xl_extention_const : str
        エクセルファイル拡張子コンスト
    kb_const : str
        キロバイトコンスト
    mail_sender_name : str
        メール差出人
    mail_sender_encode : str
        メール差出人文字コード
    """

    def __init__(self):
        self.batch_setting = OnlineBatchSetting.get_instance()
        self.smtp_user = self.batch_setting.getSmtpUser()
        self.smtp_password = self.batch_setting.getSmtpPassword()
        self.mail_subject = self.batch_setting.getMailSubject()
        self.mail_body_text = self.batch_setting.getMailBodyText()
        self.mail_from_address = self.batch_setting.getMailFromAddress()
        self.smtp_host = self.batch_setting.getSmtpHost()
        self.smtp_port = self.batch_setting.getSmtpPort()
        self.mail_keisiki = self.batch_setting.getMailKeisiki()
        self.mail_charset = self.batch_setting.getMailCharset()
        self.file_dl_url = self.batch_setting.getFileDlUrl()
        self.sys_url = self.batch_setting.getSysUrl()
        self.content_disc = 'Content-Disposition'
        self.attachment = 'attachment'
        self.xl_extention_const = '.xlsx'
        self.kb_const = 'KB'
        self.mail_sender_name = self.batch_setting.getMailSenderName()
        self.mail_sender_encode = self.batch_setting.getMailSenderEncode()

    def mailSender(self, cur, user_id, result_file_num):
        """
        添付ファイル付きメール送信の実行

        Parameters
        ----------
        cur : MySQLdb.connections.Connection
            DBカーソル
        user_id : str
            ユーザーID
        result_file_num : str
            ファイル番号
        """

        try:
            mail_dao: MailSendDao = MailSendDaoImple()
            mail_to_address = mail_dao.getMailAddress(cur, user_id)
            tmp_file_path = mail_dao.getFilePath(cur, result_file_num)
            file_gyomu_list = mail_dao.getFileGyomuData(cur, result_file_num)

            smtpobj = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtpobj.starttls()
            smtpobj.login(self.smtp_user, self.smtp_password)

            with open(tmp_file_path, 'rb') as f:
                tmp_file_byte = f.read()
            mb = MIMEApplication(tmp_file_byte)
            filename = result_file_num+self.xl_extention_const
            mb.add_header(self.content_disc, self.attachment, filename=filename)
            tmp_file_kb = str('{:.1f}'.format(len(tmp_file_byte)/1000))+self.kb_const

            self.mail_subject = self.mail_subject.format(result_file_num)
            self.file_dl_url = self.file_dl_url.format(result_file_num)
            self.mail_body_text = self.mail_body_text.format(
                user_id,
                result_file_num,
                self.file_dl_url,
                filename,
                tmp_file_kb,
                file_gyomu_list["target_start_year"],
                file_gyomu_list["target_end_year"],
                file_gyomu_list["target_start_month"],
                file_gyomu_list["target_end_month"],
                file_gyomu_list["target_ken"],
                file_gyomu_list["target_md_item"].replace(',,', ''),
                self.smtp_user,
                self.sys_url)

            msg = MIMEMultipart()
            msg['Subject'] = self.mail_subject
            msg['From'] = '%s <%s>'%(Header(self.mail_sender_name.encode(self.mail_sender_encode),self.mail_sender_encode).encode(), self.mail_from_address)
            msg['To'] = mail_to_address
            msg['Date'] = formatdate()
            msg.attach(MIMEText(self.mail_body_text, self.mail_keisiki, self.mail_charset))
            msg.attach(mb)

            smtpobj.send_message(msg)
            smtpobj.close()
        except:
            pass