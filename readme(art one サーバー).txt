

■概要------------------------------------------------------

■RDBを作成--------------------------------------------------------

■RDBとローカルマシンを接続----------------------------------------
https://cloud.google.com/sql/docs/mysql/connect-instance-auth-proxy?hl=ja

■デプロイ方法（APIサーバー）----------------------------------------------------

・config.pyのmodeを下記のように設定する
mode = "release"

・下記のコマンドでインストールされてるライブラリのリストを書き出す
pip freeze > requirements.txt

・下記のコマンドでCloud Runへのデプロイを実行する
gcloud run deploy

・下記のように表示されるのでそのままエンターを押す
Source code location (C:\Users\mmlab\Desktop\UsingDoc\draft_gallery_guide\server_side):

・作成するサーバー名を聞かれるので「art-one-api」と入力する
Service name (serverside): art-one-api

・未認証の呼び出しを許可するか聞かれるのでy
Allow unauthenticated invocations to [art-one-api] (y/N)?  y

・config.pyのmodeを元に戻る
mode = "debug"


■起動方法(開発用ローカルマシン)------------------------------------
・config.pyを修正する

・データベースを作成する
照合順序は「utf8mb4_unicode_ci」を使うこと
utf8mb4: 一文字を1～4バイトで表す。utf8は1～3バイトで本当のUTF-8ではない。
_ci: 大文字と小文字を区別しない

・DBにユーザーを作成する

・DBにテーブルを作成する
pythonの対話モードで下記のコードを順番に実行します。
python
from flaskr.__init__ import app
from flaskr.main import db
from flaskr.main import create_db
create_db()
exit()

・起動
$Env:FLASK_APP="app"
flask run --debug
flask --app flaskr/__init__  run

・テストデータを挿入する（オプション）
「POST http://127.0.0.1:5000/api/1.0/debug/insert_test_data」を実行してテストデータを挿入する


#-------------------------------------------

#Art One Apiサーバーを起動
#この方法で起動すると、APIサーバーにアクセスする場合、httpsだとエラーになります。
#httpで接続する事。
sudo flask --app "flaskr" run --port 80 --host 0.0.0.0

#リモートでバッグをするときはトンネルリンクを作成しSSH接続する
#5678はdebugpyのデフォルトのポート番号です。
ssh -i "./ssh/aws_mega.pem" -L 5678:localhost:5678 ubuntu@ec2-54-208-69-174.compute-1.amazonaws.com
ssh -i "./ssh/aws_mega.pem" -L 5678:localhost:5678 ubuntu@ec2-52-55-95-96.compute-1.amazonaws.com

#VSCodeからサーバーにPython拡張機能をインストールする


■データベースの設定-----------------------------------------

・データベースを作成する
照合順序は「utf8mb4_unicode_ci」を使うこと
utf8mb4: 一文字を1～4バイトで表す。utf8は1～3バイトで本当のUTF-8ではない。
_ci: 大文字と小文字を区別しない


■命名規則------------------------------------------------------
    ■URL
        例
        /api/1.0/media/next_id

        ハイフンではなく、アンダースコアを使う。
        参考: Twitter REST API V2

    ■URLの引数
        ?param-name=val
    ■dbのテーブル名
        table_name
    ■dbのカラム名
        column_name
    ■フォームの要素名
        param-name
    ■JSON
    {
        "foo_val": 1
    }
    
■参考------------------------------------------------------
Twitter REST API 2.0: https://developer.twitter.com/en/docs/api-reference-index