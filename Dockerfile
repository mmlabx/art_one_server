#起動方法
#-e: 環境変数の指定
#docker run <コンテナの識別子> -e <環境変数のキー>=<環境変数の値
#docker run art-one-api

FROM python:3.10-slim

#pipをアップデート
RUN pip install --upgrade pip

#標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED True

#プログラムファイルをコピーする
ENV APP_HOME /.
WORKDIR $APP_HOME
COPY . ./

#ライブラリをインストールする
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

#コンテナのポートを開放
EXPOSE 8080

#プログラムを起動する
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app