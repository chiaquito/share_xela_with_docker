# django_prod_with_docker_Sample

## 構造
```
django_prod_with_docker
├── README.md
├── app
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── app1
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── app2
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── db.sqlite3
│   ├── entrypoint.prod.sh
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── mypro
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-37.pyc
│   │   │   └── settings.cpython-37.pyc
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── requirements.txt
├── docker-compose.prod.yml
├── docker-compose.yml
└── nginx
    ├── Dockerfile
    └── nginx.conf
```

## 使い方
dockerとdocker-composeのダウンロード
1. dockerのインストール  
https://docs.docker.com/docker-for-mac/install/ からインストール
2. docker-composeのインストール
```
$ curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
$ chmod +x /usr/local/bin/docker-compose
```

起動する  
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```

実行しているサービスのチェック
```
$ docker-compose ps

$ docker-compose logs
```

サービスを停止する
```
$ docker-compose -f docker-compose.prod.yml down -v
```



## 既に開発中のdjangoプロジェクトをこのdocker環境と統合する方法


djangoのプロジェクトのルートディレクトリにrequirements.txt, entrypoint.sh, Dockerfile, docker-compose.ymlを追加する。そしてrequirements.txtにはprojectで必要なライブラリを記述する。
プロジェクトのsettings.pyの環境変数をdocker-compose.ymlに記述する。
変更内容はdbの各項目とsecret-key, DEBUGである。
そしてsettings.pyにおいてdocker-composeで定めた環境変数を取得するコードに変更する。

  

やっていることとしてdocker-compose.ymlで環境変数を設定する。これは各サービス(WebApplicationServer, DatabaseServer)のenvironmentディレクティブに記述する。   
この環境変数をdjangoプロジェクトのsettings.pyで
```
SECRET_KEY = os.environ.get('SECRET_KEY')
```
のような形で環境変数を取得する。

## このリポジトリを作成して分かったこと
dockerを使わないdjagoの環境ではプロジェクトの起動には例えばmacではpostgresqlやpythonを入れないと使えなかった。しかしながらdocker-compose.ymlやDockerfileからミドルウエアのイメージをコンテナ化、実行する。したがってmacにpostgresqlが存在していなくても起動することができるようになる事がわかった。


## 開発環境と異なる点
開発環境の環境から変更する項目が多いと感じた。

### 新規作成したディレクトリ、ファイル

 1. app/Dockerfile.prod.yml
 1. app/entrypoint.prod.sh
 1. nginx
 1. nginx/Dockerfile
 1. nginx/nginx.conf
 1. docker-compose.prod.yml
 1. .env
 1. .env.db

1 app/Dockerfile.prod.ymlでは基本的に開発環境用のapp/Dockerfile.ymlの内容と同じである。異なる点はサービスを開始したときのエントリポイントのファイルコピーすることを読み込むこと。   
```
# entrypoint.prod.shをコピー
COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.prod.sh
# entrypoint.prod.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
```
に変更すること。  

2. app/entrypoint.prod.sh
3. nginx... WebServerのサービスを実行するためのディレクトリを作成
4. nginx/Dockerfile...nginxのイメージを作成するためにファイルを作成する。  
5. nginx/nginx.conf
6. docker-compose.prod.yml...　WebApplicationServerの注意点はcommandで
```
- python manage.py runserver
+ gunicorn config.wsgi:application --bind 127.0.0.1:8000
```
environmentディレクティブを削除してenv_fileディレクティブを追加する。読み込みファイルは.env
```
- environment:
-   - DATABASE_HOST: hoge
- 省略
+ env_file: .env
```
volumesでstatic_fileのディレクトリをボリュームを追加する。このボリュームをnginxと共有することでstaticファイルをnginxを通じて配信できるようになる。

dbのサービスではアプリケーションの設定項目ではなくsbに接続するための諸項目をenv_file: .env.dbとして読み込むように変更する。

nginxではvolumesにおいて static_volume:/usr/src/app/staticを追加する。

共通のボリュームとしてstatic_volumeを追加する。


### 変更したファイル(変更概要)
 1. app/settings.py(追加)
 1. app/requirements.txt(追加)


1. app/settings.pyにはstaticファイルをnginxから配信する内容を書く。
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

2. app/requirements.txtにはgunicornによるサービス開始をするためのモジュールを追加する。
```
gunicorn==19.9.0
```



## アプリの説明
地元の情報共有サイトです。自分のいらないもの等を記事として投稿し地域の欲しい人を探せます。ジモティーのようなものです。  
自分のいらないもの以外にも部屋を貸したり、部屋を探しているという記事を作ったり需給の双方向から記事を作成する事ができます。
カテゴリーとしては以下のものがあります。

 - 自分のいらないものを売る、寄付する
 - 自分が欲しいものや困っている
 - イベントやコミュニティなどを知らせる
 - 部屋を貸す
 - 部屋を借りたい
 - 下宿したい人に住まい食事を提供する
 - 下宿したい
 - 求人を出す
 - 仕事を探す
 - 事業やお店の宣伝をする


## 機能の説明

- 記事投稿機能
- 記事編集機能
- 記事削除機能
- 記事へのお気に入り機能
- 記事をSNSでシェアする機能
- 記事検索機能(カテゴリー、地域&カテゴリー、文字列検索)
- 記事に対しコメントで交流する機能
- 取引相手を定めた場合クローズな環境でメッセージをやり取りする機能
- 記事作成者が取引地点やエリア情報を提供した場合に地図を表示する
- パスワードを忘れてしまったり、サイトにコンタクトを送った場合にメールにて対応する機能
- 記事にコメントがついた時、記事に対し取引相手候補が現れた時、クローズな環境でメッセージを受信した時、取引相手として選ばれた時にはユーザーに通知する機能。通知はAndroidではpush通知、webではブラウザのナブバーに通知がある旨を表示させる。またEmailによる通知も送信される。
- 取引後feedbackを残す機能とユーザー毎にfeedbackを閲覧する機能
- PCによるwebブラウザの表示とスマホによるwebブラウザとAndroidアプリによる表示で閲覧する事ができる。



## アプリの構成
Web:
  - WebServer:
      - nginx

  - WebApplicationServar
      - Django(Python)
      - Vue.js(javascript)

  - Database
      - Postgesql(Postgis)

AndroidApplication
  -  Kotlin
