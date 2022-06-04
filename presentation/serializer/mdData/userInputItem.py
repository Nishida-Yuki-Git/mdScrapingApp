from rest_framework import serializers
from application.service.mdData.userInputItemService import UserInputItemGetService
from application.service.mdData.Impl.userInputItemServiceImpl import UserInputItemGetServiceImpl


class YearManageMTSerializer(serializers.ModelSerializer):
    """ 気象データ収集対象年管理マスタセリアライズクラス
    """

    class Meta:
        """ 気象データ収集対象年管理マスタメタクラス
        """

        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getYearManageMTModel()
        fields = ('year_param',)


class MonthManageMTSerializer(serializers.ModelSerializer):
    """ 気象データ収集対象月管理マスタセリアライズクラス
    """

    class Meta:
        """ 気象データ収集対象月管理マスタメタクラス
        """

        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getMonthManageMTModel()
        fields = ('month_param',)


class KenParamMTSerializer(serializers.ModelSerializer):
    """ 県名管理マスタセリアライズクラス
    """

    class Meta:
        """ 県名管理マスタメタクラス
        """

        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getKenParamMTModel()
        fields = ('ken_name',)


class MDItemMTSerializer(serializers.ModelSerializer):
    """ 気象データ項目名称管理マスタセリアライズクラス
    """

    class Meta:
        """ 気象データ項目名称管理マスタメタクラス
        """

        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getMDItemMTModel()
        fields = ('md_item',)


class ProcessResultDataSerializer(serializers.ModelSerializer):
    """ ユーザー処理結果管理データセリアライズクラス
    """

    class Meta:
        """ ユーザー処理結果管理データメタクラス
        """

        service : UserInputItemGetService = UserInputItemGetServiceImpl()
        model = service.getProcessResultDataModel()
        fields = ('result_file_num','user_id','file_create_status','create_date_time',)


class UserInputItemCommunicater():
    """
    画面表示用ユーザーデータセリアライズクラス

    Attributes
    ----------
    user_id : str
        ユーザーID
    """

    def __init__(self, user_id):
        """
        Parameters
        ----------
        user_id : str
            ユーザーID
        """

        self.user_id = user_id

    def getYearManageMTObj(self):
        """
        気象データ収集対象年管理データをview層に受け渡し

        Returns
        ----------
        dict
            気象データ収集対象年管理データの全レコード
        """

        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getYearManageMTObj()
        except:
            raise

    def getMonthManageMTObj(self):
        """
        気象データ収集対象月管理データをview層に受け渡し

        Returns
        ----------
        dict
            気象データ収集対象月管理データの全レコード
        """

        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getMonthManageMTObj()
        except:
            raise

    def getKenParamMTObj(self):
        """
        県管理マスタをview層に受け渡し

        Returns
        ----------
        dict
            県管理マスタの全レコード
        """

        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getKenParamMTObj()
        except:
            raise

    def getMDItemMTObj(self):
        """
        気象データ項目名称管理マスタをview層に受け渡し

        Returns
        ----------
        dict
            気象データ項目名称管理マスタの全レコード
        """

        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl()
            return service.getMDItemMTObj()
        except:
            raise

    def getProcessResultDataObj(self):
        """
        ユーザー処理結果情報管理データをview層に受け渡し

        Returns
        ----------
        dict
            ユーザー処理結果情報管理データの、ユーザーIDに紐づく全レコード
        """

        try:
            service : UserInputItemGetService = UserInputItemGetServiceImpl(self.user_id)
            return service.getProcessResultDataObj()
        except:
            raise




