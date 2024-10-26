
import os

mode = "debug"


#RDB関連------------------------------

db_host = "localhost"   #※「http://」は付けない事！
db_name = "gallery_guide"   #DB名
db_user = 'mega'            #ログインユーザー名
db_password = "rockman"       #ログインパスワード


#画像を保存するFirebase Cloud Strage------------------------------
FBStorage = "gallery-log-859ae.appspot.com" #if os.getenv('MMLAB_DEBUG') else "localhost:9199"

#------------------------------------------------------


#接続するCloud SQLインスタンスを指定
#Cloud SQLインスタンス詳細画面の[接続名]からでも確認できます。
db_instance_connection_name = ""