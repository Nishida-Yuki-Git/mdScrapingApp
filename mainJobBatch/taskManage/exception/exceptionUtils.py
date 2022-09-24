import traceback
from mainJobBatch.taskManage.exception.mdException import MdException
from mainJobBatch.taskManage.exception.mdException import MdBatchSystemException
from mainJobBatch.taskManage.exception.mdException import MdQueBizException

class ExceptionUtilsClassSingleton(object):
    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

class ExceptionUtils(ExceptionUtilsClassSingleton):
    """
    例外発生時のハンドリングメソッド定義

    Attribute
    ---------------
    ex_kbn_MdException : str
        MdException区分
    ex_kbn_MdBatchSystemException : str
        MdBatchSystemException区分
    ex_kbn_MdQueBizException : str
        MdQueBizException区分
    """

    def __init__(self):
        self.ex_kbn_MdException = '0'
        self.ex_kbn_MdBatchSystemException = '1'
        self.ex_kbn_MdQueBizException = '2'

    def commonHandling(self, ex, ex_kbn):
        """
        例外発生時ハンドリング処理

        Parameters
        ---------------
        ex : ?
            例外インスタンス
        exKbn : str
            システム例外区分
        """

        error_text = " ".join(traceback.format_exception(type(ex), ex, ex.__traceback__))

        if ex_kbn == self.ex_kbn_MdException:
            ex = MdException()
        elif ex_kbn == self.ex_kbn_MdBatchSystemException:
            ex = MdBatchSystemException()
        elif ex_kbn == self.ex_kbn_MdQueBizException:
            ex = MdQueBizException()
        else:
            ex = MdException()

        ex.setTrace(error_text)
        return ex