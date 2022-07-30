from mainJobBatch.taskManage.serviceBase.mdScrapingMailService import MdScrapingMailService
from meteorologicalDataScrapingApp.job_config import OnlineBatchSetting
from mainJobBatch.taskManage.dao.mailSendDao import MailSendDao
from mainJobBatch.taskManage.dao.daoImple.mailSendDaoImple import MailSendDaoImple
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class MdScrapingMailServiceImpl(MdScrapingMailService):
    """
    気象データ収集メール送信サービス基底実装クラス

    Attributes
    ----------
    batch_setting : OnlineBatchSetting
        バッチ設定ファイル
    smtp_user : str
        メールサーバーログインユーザー
    smtp_password : str
        メールサーバーパスワード
    mail_subject : str
        メール件名
    mail_body_text : str
        メール本文
    mail_from_address : str
        メール送信元アドレス
    smtp_host : str
        SMTPサーバーホストアドレス「
    smtp_port : str
        SMTPサーバーポート番号
    mail_keisiki : str
        メール形式
    mail_charset : str
        メール送信時文字コード
    content_disc : str
        content_discコンスト文字列
    attachment : str
        attachmentコンスト文字列
    """

    def __init__(self):
        self.batch_setting = OnlineBatchSetting()
        self.smtp_user = self.batch_setting.getSmtpUser()
        self.smtp_password = self.batch_setting.getSmtpPassword()
        self.mail_subject = self.batch_setting.getMailSubject()
        self.mail_body_text = self.batch_setting.getMailBodyText()
        self.mail_from_address = self.batch_setting.getMailFromAddress()
        self.smtp_host = self.batch_setting.getSmtpHost()
        self.smtp_port = self.batch_setting.getSmtpPort()
        self.mail_keisiki = self.batch_setting.getMailKeisiki()
        self.mail_charset = self.batch_setting.getMailCharset()
        self.content_disc = 'Content-Disposition'
        self.attachment = 'attachment'

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

        mail_dao: MailSendDao = MailSendDaoImple()
        mail_to_address = mail_dao.getMailAddress(cur, user_id)
        tmp_file_path = mail_dao.getFilePath(cur, result_file_num)

        smtpobj = smtplib.SMTP(self.smtp_host, self.smtp_port)
        smtpobj.starttls()
        smtpobj.login(self.smtp_user, self.smtp_password)

        msg = MIMEMultipart()
        msg['Subject'] = self.mail_subject
        msg['From'] = self.mail_from_address
        msg['To'] = mail_to_address
        msg['Date'] = formatdate()
        msg.attach(MIMEText(self.mail_body_text, 'plain', 'utf-8'))

        # 添付ファイルの設定
        filename = '作成気象データファイル.xlsx'
        with open(tmp_file_path, 'rb') as f:
            mb = MIMEApplication(f.read())
        mb.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(mb)

        # 作成したメールを送信
        smtpobj.send_message(msg)
        smtpobj.close()

