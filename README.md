# 気象データ明細出力_サーバーサイドAPI

## システム概要
画面で指定した年・月・地域の気象データを収集し、エクセルファイルとしてダウンロードできるシステムです。

## パッケージ構成

```bash
$ tree
.
├── README.md
│
├── application #オンラインビジネスロジック及び永続化レポジトリインターフェースを管理
│   ├── __init__.py
│   ├── __pycache__
│   ├── repository #永続化レポジトリインターフェース
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── account #認証系永続化レポジトリインターフェース
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   └── account_repository.py
│   │   ├── mdData #ビジネス系永続化レポジトリインターフェース
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── errorRequest_repository.py
│   │   │   ├── fileDownload_repository.py
│   │   │   ├── mainBusiness_repository.py
│   │   │   └── userInputItem_repository.py
│   │   └── util #汎用系永続化レポジトリインターフェース
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       ├── generalCode_repository.py
│   │       └── saiban_repository.py
│   └── service #オンラインビジネスロジック
│       ├── __init__.py
│       ├── __pycache__
│       ├── account #認証系ロジック
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   ├── accountService.py
│       │   └── impl
│       │       ├── __init__.py
│       │       └── accountServiceImpl.py
│       ├── dto #ServiceDto
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   └── mainBusinessServiceDto.py
│       ├── enum #起動バッチ区分の列挙型を管理
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   └── exeBatchType.py
│       └── mdData #ビジネスロジック
│           ├── Impl
│           │   ├── __init__.py
│           │   ├── errorRequestServiceImpl.py
│           │   ├── fileDownloadServiceImpl.py
│           │   ├── mainBusinessServiceImpl.py
│           │   └── userInputItemServiceImpl.py
│           ├── __init__.py
│           ├── __pycache__
│           ├── errorRequestService.py
│           ├── fileDownloadService.py
│           ├── mainBusinessService.py
│           └── userInputItemService.py
│
├── cip_key.txt #暗号復号化キー管理ファイル(実際のキーはGit管理対象外)
│
├── commonUtils #システム共通部品
│   ├── __init__.py
│   └── cryptUtils #暗号復号化部品
│       ├── __init__.py
│       ├── decrypt.py
│       └── encrypt.py
│
├── error_log.txt #デバッグトレース内容出力用ファイル
│
├── mainJobBatch #随時バッチ
│   ├── __init__.py
│   ├── __pycache__
│   └── taskManage
│       ├── __init__.py
│       ├── __pycache__
│       ├── dao #Dao層
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   ├── daoImple
│       │   │   ├── __init__.py
│       │   │   ├── __pycache__
│       │   │   ├── errorFileCreateDaoImple.py
│       │   │   ├── mailSendDaoImple.py
│       │   │   ├── mdScrapingDaoImple.py
│       │   │   └── newFileCreateDaoImple.py
│       │   ├── errorFileCreateDao.py
│       │   ├── mailSendDao.py
│       │   ├── mdScrapingDao.py
│       │   └── newFileCreateDao.py
│       ├── exception #エラーハンドリングクラス
│       │   ├── __init__.py
│       │   ├── exceptionUtils.py
│       │   └── mdException.py
│       ├── job #バッチ起動クラス
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   └── jobExecute.py
│       ├── service #バッチ個別サービス実装
│       │   ├── Impl
│       │   │   ├── __init__.py
│       │   │   ├── errorFileCreateTaskServiceImpl.py
│       │   │   └── newFileCreateTaskServiceImpl.py
│       │   └── __pycache__
│       ├── serviceBase #バッチ共通基底サービス
│       │   ├── Impl
│       │   │   ├── __init__.py
│       │   │   ├── mdScrapingLogicServiceImpl.py
│       │   │   ├── mdScrapingMailServiceImpl.py
│       │   │   ├── mdScrapingTaskServiceImpl.py
│       │   │   └── mdScrapingXlWriteServiceImpl.py
│       │   ├── __init__.py
│       │   ├── mdScrapingLogicService.py
│       │   ├── mdScrapingMailService.py
│       │   ├── mdScrapingTaskService.py
│       │   └── mdScrapingXlWriteService.py
│       └── task #タスクコントローラー
│           ├── __init__.py
│           ├── __pycache__
│           ├── base
│           │   ├── __init__.py
│           │   ├── __pycache__
│           │   └── mdScrapingTask.py
│           ├── errorFileCreateTask.py
│           └── newFileCreateTask.py
│
├── manage.py #オンラインシステムメインプロセス起動
│
├── media #随時バッチで作成したファイルの格納場所
│   └── file
│
├── meteorologicalDataScrapingApp #オンライン・バッチそれぞれの設定ファイルを管理
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-37.pyc
│   │   ├── settings.cpython-37.pyc
│   │   ├── urls.cpython-37.pyc
│   │   └── wsgi.cpython-37.pyc
│   ├── asgi.py
│   ├── job_config.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── presentation #ルーティング及びJSONデータのIn/Out処理を行う
│   ├── __init__.py
│   ├── __pycache__
│   ├── apps.py
│   ├── enum #enum型定義
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── resStatusCode.py
│   ├── serializer #認証系とビジネス系それぞれのシリアライズ
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── account
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   └── account.py
│   │   └── mdData
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       ├── errorRequest.py
│   │       ├── fileDownload.py
│   │       ├── mainBusiness.py
│   │       └── userInputItem.py
│   ├── url #ルーティング設定
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── account.py
│   │   └── mdData.py
│   └── view #JSONデータのIn/Out、View単位のトランザクション管理等を行う
│       ├── __init__.py
│       ├── __pycache__
│       ├── account.py
│       └── mdData.py
│
├── requirements.txt #プロジェクトで使用しているライブラリのバージョン管理ファイル
│
├── scrapingSystem #スキーマ管理や永続化処理、オフラインバッチコマンドの管理等を行う
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-37.pyc
│   │   ├── admin.cpython-37.pyc
│   │   ├── apps.cpython-37.pyc
│   │   ├── forms.cpython-37.pyc
│   │   ├── models.cpython-37.pyc
│   │   ├── urls.cpython-37.pyc
│   │   └── views.cpython-37.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── management #オフラインバッチ管理フォルダ
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── commands
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       └── masterSetting.py
│   ├── migrations #マイグレーション管理フォルダ
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20211221_2137.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-37.pyc
│   │       ├── 0002_mditemmt.cpython-37.pyc
│   │       ├── 0003_userdata.cpython-37.pyc
│   │       ├── 0004_auto_20211105_2200.cpython-37.pyc
│   │       ├── 0005_auto_20211105_2202.cpython-37.pyc
│   │       └── __init__.cpython-37.pyc
│   ├── models.py #スキーマテーブル定義ソース
│   └── repositoryImple #認証系、ビジネス系、汎用系それぞれのレポジトリ実装
│       ├── __init__.py
│       ├── __pycache__
│       ├── account
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   └── account_repository.py
│       ├── mdData
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   ├── errorRequest_repository.py
│       │   ├── fileDownload_repository.py
│       │   ├── mainBusiness_repository.py
│       │   └── userInputItem_repository.py
│       └── util
│           ├── __init__.py
│           ├── __pycache__
│           ├── generalCode_repository.py
│           └── saiban_repository.py
│
├── static
│
└── staticfiles
```
 
## システムURL
http://www.md-data.net/sendPost  
(上記は本システムのフロントシステムURLで、サーバーサイドAPIにはフロントシステムのサーバー内でアクセスします) 
https://tranquil-meadow-43680.herokuapp.com/sendPost  
(SSL認証がされているURLは上記になります。SSL認証URLのみアクセス可能な場合は上記からアクセスをお願いいたします。)


## その他システムの情報
・システムの処理概要  
・オンライン, バッチそれぞれのアーキテクチャ  
・ER図  
・トランザクジョン管理方式  
・インフラ, ネットワーク構成  

上記の情報及びその他本システムの情報については、  
**気象データ明細出力システム_システム設計ドキュメントレポジトリ**を参照してください。
