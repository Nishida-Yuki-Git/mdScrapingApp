class ResStatusCode():
    """ ステータスコードconst
    """

    @staticmethod
    def getSuccessCode():
        """
        ステータスコード(処理成功)の返却

        Returns
        ----------
        success_code : str
            ステータスコード(処理成功)
        """

        success_code = 0
        return success_code

    @staticmethod
    def getErrorCode():
        """
        ステータスコード(処理失敗)の返却

        Returns
        ----------
        success_code : str
            ステータスコード(処理失敗)
        """

        error_code = 1
        return error_code