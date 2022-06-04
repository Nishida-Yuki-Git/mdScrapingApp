# 気象データ明細出力_サーバーサイドAPI

## システム概要
画面で指定した年・月・地域の気象データを収集し、エクセルファイルとしてダウンロードできるシステムです。

## パッケージ構成(一部省略)

```bash
$ tree
.
├── application #オンラインビジネスロジック及び永続化レポジトリインターフェースを管理
│   ├── repository #永続化レポジトリインターフェース
│   │   ├── account #認証系永続化レポジトリインターフェース
│   │   │   └── account_repository.py
│   │   ├── mdData #ビジネス系永続化レポジトリインターフェース
│   │   │   ├── errorRequest_repository.py
│   │   │   ├── fileDownload_repository.py
│   │   │   ├── mainBusiness_repository.py
│   │   │   └── userInputItem_repository.py
│   │   └── util #汎用系永続化レポジトリインターフェース
│   │       ├── generalCode_repository.py
│   │       └── saiban_repository.py
│   └── service #オンラインビジネスロジック
│       ├── account #認証系ロジック
│       │   ├── accountService.py
│       │   └── impl
│       │       └── accountServiceImpl.py
│       ├── dto
│       │   └── mainBusinessServiceDto.py #メインビジネスロジック(新規ファイル作成)で使用するserviceDto
│       ├── enum
│       │   └── exeBatchType.py #起動バッチ区分の列挙型
│       └── mdData #ビジネスロジック
│           ├── Impl
│           │   ├── errorRequestServiceImpl.py
│           │   ├── fileDownloadServiceImpl.py
│           │   ├── mainBusinessServiceImpl.py
│           │   └── userInputItemServiceImpl.py
│           ├── errorRequestService.py
│           ├── fileDownloadService.py
│           ├── mainBusinessService.py
│           └── userInputItemService.py
├── error_log.txt #デバッグトレース内容出力用ファイル(本番環境専用)
├── mainJobBatch #随時バッチ
│   └── taskManage
│       ├── dao
│       │   ├── daoImple
│       │   │   ├── errorFileCreateDaoImple.py #エラーファイル再作成バッチDAO実装クラス
│       │   │   ├── mdScrapingDaoImple.py #バッチ共通Dao実装クラス
│       │   │   └── newFileCreateDaoImple.py #新規ファイル作成バッチDAO実装クラス
│       │   ├── errorFileCreateDao.py #エラーファイル再作成バッチDAOインターフェース
│       │   ├── mdScrapingDao.py #バッチ共通DAOインターフェース
│       │   └── newFileCreateDao.py #新規ファイル作成バッチDAOインターフェース
│       ├── job
│       │   └── jobExecute.py #起動バッチを判別してバッチ処理を開始する
│       ├── service #サービス
│       │   └── Impl
│       │       ├── errorFileCreateTaskServiceImpl.py #エラーファイル再作成バッチタスクサービス
│       │       └── newFileCreateTaskServiceImpl.py #新規ファイル作成バッチタスクサービス
│       ├── serviceBase #基底サービス
│       │   ├── Impl
│       │   │   ├── mdScrapingLogicServiceImpl.py #ビジネスロジックサービスクラス
│       │   │   └── mdScrapingTaskServiceImpl.py #バッチ共通タスクサービス基底クラス 
│       │   ├── mdScrapingLogicService.py #ビジネスロジックサービスインターフェース
│       │   └── mdScrapingTaskService.py #バッチ共通タスクサービス基底インターフェース
│       └── task #タスクコントローラー
│           ├── base
│           │   └── mdScrapingTask.py #バッチ共通タスクコントローラー基底クラス
│           ├── errorFileCreateTask.py #エラーファイル再作成バッチタスクコントローラー
│           └── newFileCreateTask.py #新規ファイル作成バッチタスクコントローラー
├── manage.py #オフラインバッチ起動ソース
├── media #バッチで作成したエクセルファイルの格納場所
│   └── file
├── meteorologicalDataScrapingApp
│   ├── asgi.py
│   ├── job_config.py #随時バッチ設定ファイル
│   ├── settings.py #オンライン設定ファイル
│   ├── urls.py #ルーティング設定
│   └── wsgi.py
├── presentation #ルーティング及びJSONデータのIn/Out処理を行う
│   ├── apps.py
│   ├── enum
│   │   └── resStatusCode.py #レスポンス時のステータス定義
│   ├── serializer #認証系とビジネス系それぞれのシリアライズ
│   │   ├── account
│   │   │   └── account.py
│   │   └── mdData
│   │       ├── errorRequest.py
│   │       ├── fileDownload.py
│   │       ├── mainBusiness.py
│   │       └── userInputItem.py
│   ├── url #ルーティング設定
│   │   ├── account.py
│   │   └── mdData.py
│   └── view #JSONデータのIn/Out等のメイン処理、View単位のトランザクション管理等を行う
│       ├── account.py
│       └── mdData.py
├── requirements.txt #プロジェクトで使用しているライブラリのバージョン管理ファイル(本番環境で使用)
├── scrapingSystem #スキーマ管理や永続化処理、オフラインバッチコマンドの管理等を行う
│   ├── admin.py #管理画面の設定
│   ├── apps.py
│   ├── management #オフラインバッチ管理フォルダ
│   │   └── commands
│   │       └── masterSetting.py #トランとマスタの初期化バッチ
│   ├── migrations #マイグレーション管理フォルダ
│   ├── models.py #DBスキーマ定義ソース
│   └── repositoryImple #認証系、ビジネス系、汎用系それぞれのレポジトリ実装
│       ├── account
│       │   └── account_repository.py
│       ├── mdData
│       │   ├── errorRequest_repository.py
│       │   ├── fileDownload_repository.py
│       │   ├── mainBusiness_repository.py
│       │   └── userInputItem_repository.py
│       └── util
│           ├── generalCode_repository.py
│           └── saiban_repository.py
├── static #デプロイ時のcollectStatic用ディレクトリ
└── staticfiles #デプロイ時のcollectStatic用ディレクトリ
```
 
## システムURL
http://www.md-data.net/sendPost  
(上記は本システムのフロントシステムURLで、サーバーサイドAPIにはフロントシステムのサーバー内でアクセスします)


## その他システムの情報
・システムの処理概要  
・オンライン, バッチそれぞれのアーキテクチャ  
・ER図  
・トランザクジョン管理方式  
・インフラ, ネットワーク構成  

上記の情報及びその他本システムの情報については、  
**気象データ明細出力システム_システム設計ドキュメントレポジトリ**を参照してください。
