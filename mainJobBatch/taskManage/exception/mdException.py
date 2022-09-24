class MdException(Exception):
    """
    オンライン随時バッチ基底例外

    Attributes
    ----------
    ex_output_message_base : str
        例外出力メッセージ基盤
    ex_prace : str
        埋め込み文字列(子どもExceptionで具体的には定義する)
    trace_text : str
        スタックトレース全文
    """

    def __init__(self):
        self.ex_output_message_base = '{0}エラーが発生しました'
        self.ex_prace = ''
        self.trace_text = ''

    def getMessage(self):
        return self.ex_output_message_base.format(self.ex_prace)
    def getTrace(self):
        return self.trace_text
    def setTrace(self, trace_text):
        self.trace_text = trace_text

class MdBatchSystemException(MdException):
    """
    バッチ基盤処理例外

    Attributes
    ----------
    ex_prace : str
        埋め込み文字列
    """

    def __init__(self):
        super().__init__()
        self.ex_prace = 'MdBatchSystemException_バッチシステム基盤'

class MdQueBizException(MdException):
    """
    バッチキュービジネスロジック例外

    Attributes
    ----------
    ex_prace : str
        埋め込み文字列
    """

    def __init__(self):
        super().__init__()
        self.ex_prace = 'MdQueBizException_バッチキュービジネスロジック'