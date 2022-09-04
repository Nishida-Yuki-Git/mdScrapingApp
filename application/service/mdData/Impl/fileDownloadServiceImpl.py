from application.service.mdData.fileDownloadService import FileDownloadService
from multiprocessing import Pool

class FileDownloadServiceImpl(FileDownloadService):
    """
    ファイルダウンロードサービス実装クラス

    Attributes
    ----------
    byte_shift_num : int
        バイト配列分割lengthを決定するbitシフト数
    byte_divide_process_num ; int
        バイト配列分割プロセス並列処理数
    result_file_num : str
        ファイル番号
    xl_byte_data : list
        送信ファイルバイトデータ
    moto_byte_size : int
        送信ファイルバイトサイズ
    moto_byte_size : int
        分割バイト配列length
    byte_in_list : list
        サブプロセス収集後バイトデータint配列
    tree_list : list
        サブプロセス処理データ格納list
    process_index_que : list
        サブプロセス実行順序格納list
    start_index_list : list
        バイト配列パーティションスタートインデックスlist
    last_index_list : list
        バイト配列パーティション終了インデックスlist
    """

    def __init__(self, result_file_num):
        """
        Parameters
        ----------
        result_file_num : str
            ファイル番号
        """

        self.byte_shift_num = 3
        self.byte_divide_process_num = 8
        self.result_file_num = result_file_num
        self.xl_byte_data = []
        self.moto_byte_size = 0
        self.tree_list_length = 0
        self.byte_in_list = []
        self.tree_list = []
        self.process_index_que = []
        self.start_index_list = []
        self.last_index_list = []

    def mainLogic(self):
        """
        ファイルダウンロード実行

        Returns
        ----------
        list
            int変換後バイナリデータ
        """

        try:
            from application.repository.mdData.fileDownload_repository import FileDownloadRepository
            from scrapingSystem.repositoryImple.mdData.fileDownload_repository import FileDownloadRepositoryImple

            file_download_repo: FileDownloadRepository = FileDownloadRepositoryImple()
            user_file_obj = file_download_repo.getUserFileObject(self.result_file_num)
            user_file = user_file_obj.create_file.name

            with open(user_file, "rb") as f:
                self.xl_byte_data = f.read()
            self.moto_byte_size = len(self.xl_byte_data)
            self.tree_list_length = self.moto_byte_size>>self.byte_shift_num;

            self.__twoDevideByteData(0, (self.moto_byte_size-1))

            pool = Pool(processes=self.byte_divide_process_num)
            pool_result_list = []
            args_list = []
            for i in range(len(self.start_index_list)):
                args = (self.xl_byte_data, i, self.start_index_list[i], self.last_index_list[i],)
                args_list.append(args)
            pool_result_list = pool.map(multiByteParseStringWrapper, args_list)
            for pool_result in pool_result_list:
                self.process_index_que.append(pool_result[0])
                self.tree_list.append(pool_result[1])

            for i in range(len(self.tree_list)):
                if i==0:
                    process_que_index = self.process_index_que.index(i);
                    self.byte_in_list = self.tree_list[process_que_index]
                else:
                    process_que_index = self.process_index_que.index(i);
                    self.byte_in_list.extend(self.tree_list[process_que_index])

            return self.byte_in_list
        except:
            raise

    def __twoDevideByteData(self, start_index, last_index):
        """
        送信ファイル再起分割処理

        Parameters
        ----------
        start_index : int
            バイト配列パーティションスタートインデックス
        start_index : int
            バイト配列パーティション終了インデックス
        """
        moto_list_len = (last_index-start_index)+1
        if moto_list_len <= self.tree_list_length:
            self.start_index_list.append(start_index)
            self.last_index_list.append(last_index)
        else:
            middle_index = (last_index+start_index)>>1
            self.__twoDevideByteData(start_index, middle_index)
            self.__twoDevideByteData(middle_index+1, last_index)

def multiByteParseString(xl_byte_data, process_index, start_index, last_index):
    """
    byte->int変換処理(並列起動)

    Parameters
    ----------
    xl_byte_data : list
        元バイトデータ
    process_index : int
        poolされたプロセスの索引番号
    start_index : int
        バイト配列パーティションスタートインデックス
    start_index : int
        バイト配列パーティション終了インデックス
    """
    tree_and_process_index_que = []
    byte_parce_int_data = []
    for i in range(start_index, last_index+1):
        byte_parce_int_data.append(xl_byte_data[i])
    tree_and_process_index_que.append(process_index)
    tree_and_process_index_que.append(byte_parce_int_data)
    return tree_and_process_index_que

def multiByteParseStringWrapper(args):
    """ byte->int変換処理メソッドラッパー
    """
    return multiByteParseString(*args)

