#!/bin/sh

#Dockerをインストールする
echo "Dockerのインストールを開始します。"

sudo yum install -y docker          # dockerのインストール
sudo service docker start           # dockerの起動
sudo usermod -a -G docker ec2-user  # ec2-userをdockerグループに入れる。これでec2-userがdockerコマンドを実行できる
sudo docker info                    # dockerの起動確認

#Docker Composeをインストールする
echo "Docker Composeのインストールを開始します。"
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
