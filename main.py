#TODO オートコミットをが有効になっているようだが、明示的有効にする方法を探すこと

import copy
from urllib import response
import config
import inspect
#firebase
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials, storage
#FlaskSQLAlchemy
#■インストール
#pip install mysql-connector-python
#pip3 install flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, asc, desc, not_, or_
#その他
from flask import make_response, render_template
from flask import request
import urllib
import urllib.request
from os.path import expanduser
from flask import Flask, send_from_directory
import json
import uuid
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
import datetime
import pytz
from sqlalchemy import text
import re
import firebase_admin
from firebase_admin import firestore, auth, credentials
import time
import requests  # 「pip install requests」などが必要
from sqlalchemy.dialects.postgresql import insert  # on_conflict_do_update が使える
from sqlalchemy import func
from sqlalchemy.dialects import mysql
from enum import IntEnum, auto
import shortuuid
from sqlalchemy.dialects.mysql import LONGTEXT
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields

from flask import Flask
from flask_cors import CORS
import firebase_admin
import g
from ipwhois import IPWhois

import firebase_admin
from firebase_admin import credentials, messaging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


if g.isDebug() == True:
    print('\033[32m'+'デバッグモードで起動中です。'+'\033[0m')

if g.isRelease() == True:
    print('\033[31m' + 'リリースモードで起動中です。'+'\033[0m')


#Flaskオブジェクトを作成する
app = Flask(__name__)


#Flaskを実行する
#
#__name__は次の値になります
#   ・python パイソンファイル名でプログラムが実行された場合: "__main__"
#   ・他のパイソンプログラムからimportされた場合: __name__が書かれたパイソンファイル名
#     
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


#SQLAlchemyの為の環境変数を設定する
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "S:\SavedDoc\Dev\flutter\draft_gallery_guide\server_side\flaskr\gallery-log-859ae-firebase-adminsdk-getv2-5b2f575000.json"
#sqliteの場合
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
#mySQLの場合
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
    'user': config.db_user,
    'password': config.db_password,
    'host': config.db_host,
    'dbname': config.db_name
})

#SQLAlshemyオブジェクトを作成する
#・SQLAlshemyリファレンス https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/api.html
g.db = SQLAlchemy(app)

#Marshmallowオブジェクトを作成する
g.ma = Marshmallow(app)   #MarshmallowはSQLで取得したデータをJsonに変換するライブラリ

# データベースのテーブルの親クラスを取得
#__tablename__を使用するにはこのクラスを継承する必要がある
Base = declarative_base()

#Firebaseを初期化する--------------------------------------------------------

#Firebase Adminを初期化する
cred = credentials.Certificate("./firebase_secret_key.json") # ダウンロードした秘密鍵
firebase_admin.initialize_app(cred)

#デバッグモードだった場合の設定をする
g.setDebugSettings()

#リリースモードだった場合の設定をする
g.setReleaseSettings()

#このAPIサーバーのIPアドレスをFirestoreに保存する-------------------

def get_gip_addr():
    '''
    このAPIサーバーのIPアドレスを取得する
    '''
    res = requests.get('https://ifconfig.me')
    return res.text

#Firestoreオブジェクトを取得する
fsClient = firestore.client()

#保存先を取得する
doc_ref = fsClient.collection("art_one").document("config")

#APIサーバーのIPアドレスを保存する
doc_ref.set(
        {
            "api_server_name": "http://" + get_gip_addr()
        }
    )


#その他--------------------------------------------------------

@app.route("/get_whois", methods=["GET"])
def get_whois():
    '''
    アクセス元のWhois情報を取得する
    '''
    try:
        obj = IPWhois(request.remote_addr)
        whoisInfo = obj.lookup_whois()
        return jsonify({'whois': whoisInfo}), 200
    except Exception as e:
        print(e)

def printSql(q):
    print(
        q.statement.compile(
        dialect = mysql.dialect(),
        compile_kwargs = {
            "literal_binds": True
            }
        )
    )


def normalizeValue( container, key):
    '''
    コンテナに指定したキーが存在していれば、その値を、存在していなければNoneを返す
    '''
    try:
        res = container[key]
    except Exception as e:
        res = None
    
    return res


def assignmentEvent( event, jsonVal):
    '''
    jsonでEventを初期化する
    '''
    event.event_id = normalizeValue(jsonVal, "event_id")
    event.auther_user_id = normalizeValue(jsonVal, "auther_user_id")
    event.auther_ip = normalizeValue(jsonVal, "auther_ip")

    event.organizer_user_id = normalizeValue(jsonVal, "organizer_user_id")
    event.title = normalizeValue(jsonVal, "title")
    event.overview = normalizeValue(jsonVal, "overview")
    #住所
    event.place_id = normalizeValue(jsonVal, "place_id")

    event.google_place_id = normalizeValue(jsonVal, "google_place_id")

    event.full_address = normalizeValue(jsonVal, "full_address")
    event.country = normalizeValue(jsonVal, "country")
    event.prefecture = normalizeValue(jsonVal, "prefecture")
    event.municipality = normalizeValue(jsonVal, "municipality")
    event.sub_address = normalizeValue(jsonVal, "sub_address")
    event.building_name = normalizeValue(jsonVal, "building_name")
    event.place_name = normalizeValue(jsonVal, "place_name")
    event.rest_address = normalizeValue(jsonVal, "rest_address")

    event.latitude = normalizeValue(jsonVal, "latitude")
    event.longitude = normalizeValue(jsonVal, "longitude")
    #開催日
    event.start_date = normalizeValue(jsonVal, "start_date")
    event.end_date = normalizeValue(jsonVal, "end_date")

    event.website = normalizeValue(jsonVal, "website")
    event.rating = normalizeValue(jsonVal, "rating")
    event.age_rating = normalizeValue(jsonVal, "age_rating")


#ユーザー関連--------------------------------------------------------
#■参考
#https://gray-code.com/wordpress/getting-information-of-login-user/

class User(Base, g.db.Model):
    __tablename__ = 'users'

    user_id = g.db.Column( g.db.String(256), primary_key=True)              
    name = g.db.Column( g.db.String(128), nullable=True, default="")       #プロフィールに表示される名前
    username = g.db.Column( g.db.String(128) )                          #スクリーンネーム
    profile_media_id = g.db.Column( g.db.Integer, nullable=True)        #アバター画像のID
    biography = g.db.Column( g.db.String(2000),  default="")            #自己紹介
    birthday = g.db.Column( g.db.Date, nullable=True)                   #誕生日
    website = g.db.Column( g.db.String(2083),  nullable=True)           #Webサイト
    user_role_group_id = g.db.Column( g.db.Integer, default=3 )         #権限グループのID
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class UserSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        # モデルのプロパティ（テーブルのカラム）を全てスキーマに適用する
        model = User
        # include_relationships = True
        load_instance = True

    # create_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')


class Usermeta(Base, g.db.Model):
    __tablename__ = 'usermeta'
    user_meta_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256) )
    meta_type = g.db.Column( g.db.String(255), nullable=True )
    meta_key = g.db.Column( g.db.String(255), nullable=True )
    meta_value = g.db.Column( LONGTEXT, nullable=True )

    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class UsermetaSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usermeta
        load_instance = True


#ユーザー権限関連--------------------------------------------------------

#参考
#   ・権限の説明 ⇒ https://comcent.co.jp/blog/archives/823/

class UserRoleGroup(Base, g.db.Model):
    __tablename__ = "user_role_groups"

    user_role_group_id = g.db.Column( g.db.Integer, primary_key=True)
    role_group_name = g.db.Column( g.db.String(128) )


class UserRole(Base, g.db.Model):
    __tablename__ = "user_roles"

    user_role_id = g.db.Column( g.db.Integer, primary_key=True)
    user_role_group_id = g.db.Column( g.db.Integer )
    value = g.db.Column( g.db.String(128) )



#Like関連--------------------------------------------------------

class LikeEvent(Base, g.db.Model):
    __tablename__ = "like_events"
    like_event_id = g.db.Column( g.db.Integer, primary_key=True)
    user_id = g.db.Column( g.db.String(256), nullable=True)
    event_id = g.db.Column( g.db.Integer, nullable=True)
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))

 
class LikeUser(Base, g.db.Model):
    __tablename__ = "like_users"
    like_user_id = g.db.Column( g.db.String(256), primary_key=True)
    user_id = g.db.Column( g.db.Integer, nullable=True)
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class LikePlace(Base, g.db.Model):
    __tablename__ = "like_places"
    like_place_id = g.db.Column( g.db.String(256), primary_key=True)
    place_id = g.db.Column( g.db.Integer, nullable=True)
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))



#フォロー関連--------------------------------------------------------

class FollowUser(Base, g.db.Model):
    __tablename__ = "follow_users"
    follow_user_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.Integer, nullable=True)
    target_user_id = g.db.Column( g.db.String(256))
    memo = g.db.Column( g.db.String(256), nullable=True, default="")

class FollowPlace(Base, g.db.Model):
    __tablename__ = "follow_places"
    follow_place_id = g.db.Column( g.db.Integer, primary_key=True)
    place_id = g.db.Column( g.db.Integer, nullable=True)
    memo = g.db.Column( g.db.String(256), nullable=True, default="")


#通知関連----------------------------------------------------

class Topic(Base, g.db.Model):
    __tablename__ = "topic_list"
    topic_id = g.db.Column( g.db.Integer, primary_key=True)

    topic_name = g.db.Column( g.db.String(256))     #トピック名

class TopicSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Topic
        load_instance = True


#購読者
class Subscriber(Base, g.db.Model):
    __tablename__ = "subscriber_list"
    subscriber_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256))
    topic_id = g.db.Column( g.db.Integer)


class Notification(Base, g.db.Model):
    __tablename__ = "notification_list"
    notification_id = g.db.Column( g.db.Integer, primary_key=True)

    send_target_type = g.db.Column( g.db.String(256))   #"user_id" or "token" or "topic"
    send_target = g.db.Column( g.db.String(256))        #ユーザーID、またはトピック名
    title = g.db.Column( g.db.String(1024))             #
    body = g.db.Column( g.db.String(1024))              #
    link = g.db.Column( g.db.String(2083))              #

    #投稿日
    create_time = g.db.Column(g.db.DateTime, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))   #投稿日
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))

class NotificationScheme(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True


class DeviceToken(Base, g.db.Model):
    __tablename__ = "user_token_list"

    user_token_id = g.db.Column( g.db.Integer, primary_key=True)
    user_id = g.db.Column( g.db.String(256))
    token = g.db.Column( g.db.String(2048))

class UserTokenSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceToken
        load_instance = True


#メディア関連--------------------------------------------------------

class Media(Base, g.db.Model):
    __tablename__ = 'media'
    #メディアIDはそのままファイル名として使用されます
    media_id = g.db.Column( g.db.Integer, primary_key=True)
    auther_user_id = g.db.Column( g.db.Integer, nullable=True)  #投稿者ID
    auther_ip = g.db.Column( g.db.String(128), nullable=True, default="")
    #メディアの種類。image/jpegなど、MIMEタイプで保存する
    content_type = g.db.Column( g.db.String(128), nullable=True, default="")
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


#イベント関連--------------------------------------------------------

class Event(Base, g.db.Model):
    __tablename__ = 'events'
    
    event_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True) #ID

    auther_user_id = g.db.Column( g.db.String(256), nullable=True)          #投稿者のユーザーID
    auther_ip = g.db.Column( g.db.String(128), nullable=True, default="")   #投稿者のIPアドレス
    #
    organizer_user_id = g.db.Column( g.db.String(256), nullable=True)  #代表者のユーザーID
    title = g.db.Column( g.db.String(128), default="")                      #タイトル
    overview = g.db.Column( g.db.String(2083), nullable=True, default="")   #概要

    #住所
    place_id = g.db.Column( g.db.Integer, nullable=True)    #プレイスID

    google_place_id = g.db.Column( g.db.String(256), nullable=True, default="")     #Google Place ID

    full_address = g.db.Column( g.db.String(512), default="")     #住所全文
    country = g.db.Column( g.db.String(64), default="")  #国籍
    prefecture = g.db.Column( g.db.String(64), default="")  #都道府県
    municipality = g.db.Column( g.db.String(64), default="")  #市区町村
    sub_address = g.db.Column( g.db.String(512), default="")  #サブアドレス
    building_name = g.db.Column( g.db.String(512), default="")  #建物の名前
    place_name = g.db.Column( g.db.String(512), default="")        #場所の名前
    rest_address = g.db.Column( g.db.String(512), default="")        #住所の続き

    latitude = g.db.Column( g.db.Double, default=0.0)        #緯度
    longitude = g.db.Column( g.db.Double, default=0.0)       #経度

    #会期
    start_date = g.db.Column( g.db.Date, default=None)
    end_date = g.db.Column( g.db.Date, default=None)

    #ウェブサイト
    website = g.db.Column( g.db.String(2083), nullable=True )

    #

    #評価
    rating = g.db.Column( g.db.Double, nullable=True)        #評価

    #年齢制限
    #制限がない場合はnull
    age_rating = g.db.Column( g.db.Integer, nullable=True)

    #コメントステータス
    #【参考】https://ja.wordpress.org/support/article/post-status/
    comment_status = g.db.Column( g.db.String(20), default="open")

    #投稿ステータス
    #【参考】https://ja.wordpress.org/support/article/post-status/
    post_status = g.db.Column( g.db.String(20), default="publish")

    #open or closed
    ping_status = g.db.Column( g.db.String(20), default="open")

    #親のID
    #
    post_parent = g.db.Column( g.db.Integer, default=0 )

    #投稿タイプ
    #【参考】https://ja.wordpress.org/support/article/post-types/
    #【例】
    #   イベント: "post"
    #   更新履歴: "revision"
    post_type = g.db.Column( g.db.String(20), nullable=True, default="post")

    #投稿日
    create_time = g.db.Column(g.db.DateTime, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))   #投稿日
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class EventSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True

    # create_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')

eventMediaListTableName = "event_media"
class EventMediaList(Base, g.db.Model):
    __tablename__ = eventMediaListTableName
    event_media_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)
    event_id = g.db.Column( g.db.Integer, nullable=True )   #イベントのID
    media_id = g.db.Column( g.db.Integer, nullable=True )   #メディアのID
    index = g.db.Column( g.db.Integer, nullable=True )      #インデックス
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))

class EventMetaData(Base, g.db.Model):
    __tablename__ = "eventmeta"
    metadata_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)

    event_id = g.db.Column( g.db.Integer )      #対象となるイベントのID
    meta_key = g.db.Column( g.db.String(255) )  #キー
    meta_value = g.db.Column( LONGTEXT )      #値

class EventMetaDataSchema(g.ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventMetaData
        load_instance = True


#ブックマーク関連--------------------------------------------------------

class BookmarkGroup(Base, g.db.Model):
    __tablename__ = "bookmark_groups"
    bookmark_group_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256))    #ユーザーID
    type = g.db.Column( g.db.String(256))       #ブックマークする、イベントID、ユーザーIDなど
    name = g.db.Column( g.db.String(256))       #グループ名

    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class Bookmark(Base, g.db.Model):
    __tablename__ = "bookmarks"
    bookmark_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256))        #ユーザーID
    bookmark_group_id = g.db.Column( g.db.Integer)  #グループID
    target_id = g.db.Column( g.db.Integer)          #ブックマークする、イベントID、ユーザーIDなど
    memo = g.db.Column( g.db.String(256))           #メモ
    
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


#ブックマーク関連(ターゲットがString型バージョン)--------------------------------------------------------

class BookmarkGroupStr(Base, g.db.Model):
    __tablename__ = "bookmark_groups_str"
    bookmark_group_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256))    #ユーザーID
    type = g.db.Column( g.db.String(256))       #ブックマークする、イベントID、ユーザーIDなど
    name = g.db.Column( g.db.String(256))       #グループ名

    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


class BookmarkStr(Base, g.db.Model):
    __tablename__ = "bookmarks_str"
    bookmark_id = g.db.Column( g.db.Integer, primary_key=True)

    user_id = g.db.Column( g.db.String(256))        #ユーザーID
    bookmark_group_id = g.db.Column( g.db.Integer)  #グループID
    target_id = g.db.Column( g.db.String(256))      #ブックマークする、イベントID、ユーザーIDなど
    memo = g.db.Column( g.db.String(256))           #メモ
    
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))



#場所関連--------------------------------------------------------

class Place(Base, g.db.Model):
    __tablename__ = "places"
    placee_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)
    auther_user_id = g.db.Column( g.db.Integer, nullable=True)
    auther_ip = g.db.Column( g.db.String(128), nullable=True, default="")    
    google_place_id = g.db.Column( g.db.String(256), nullable=True, default="")    #Google Place ID
    owner_user_id = g.db.Column( g.db.Integer, nullable=True, default=0)    #オーナーのユーザーID
    #概要
    name = g.db.Column( g.db.String(512), nullable=True, default="")        #場所の名前
    #住所
    address = g.db.Column( g.db.String(512), nullable=True, default="")     #住所
    latitude = g.db.Column( g.db.Double, nullable=True, default=0.0)        #緯度
    longitude = g.db.Column( g.db.Double, nullable=True, default=0.0)       #経度
    iso_3166_2 = g.db.Column( g.db.String(4), nullable=True, default="")     #ISO 3166-2で定義された地域コード
    #投稿日
    create_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


#アクセス解析関連--------------------------------------------------------

class AnalyticsData(Base, g.db.Model):
    __tablename__ = "analytics_data"

    analytics_data_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)

    url = g.db.Column( g.db.String(2083) )  #アクセス先のURL
    access_aource_url = g.db.Column( g.db.String(2083) )  #アクセス元URL
    user_id = g.db.Column( g.db.String(256) )   #アクセス元ユーザーID
    access_source_ip = g.db.Column( g.db.String(128), default="")    #アクセス元IPアドレス

    #whois
    #TODO
    
    create_time_utc = g.db.Column(g.db.DateTime, default=datetime.datetime.now( pytz.timezone("UTC")))
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


#メタデータ関連--------------------------------------------------------

class MetaData(Base, g.db.Model):
    __tablename__ = "meta_data_list"
    
    metadata_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)

    type = g.db.Column( g.db.String(256), nullable=True, default="")       #UsersMeta, EventsMeta、など
    target_id = g.db.Column( g.db.String(256), nullable=True, default="")  #ユーザーID、イベントIDなど
    meta_key = g.db.Column( g.db.String(255) )  #キー
    meta_value = g.db.Column( LONGTEXT )      #値

    #投稿日
    create_time = g.db.Column(g.db.DateTime, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))   #投稿日
    create_time_utc = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("UTC")))


#レート（リミットステータス）関連--------------------------------------------------------
#■参考 https://syncer.jp/Web/API/Twitter/REST_API/GET/application/rate_limit_status/
class RateLimitStatus(Base, g.db.Model):
    '''
    '''
    __tablename__ = "rate_limit_status_list"

    rate_limit_status_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True)

    user_id = g.db.Column( g.db.String(256) )        #ユーザーIDまたはIPアドレスなど
    status_name = g.db.Column( g.db.String(256) )    #ステータスの名前
    remaining = g.db.Column( g.db.Integer )     #残りの数

    #最後にリミットがリセットされた時刻
    latest_reset_time = g.db.Column(g.db.DateTime, nullable=True, default=datetime.datetime.now( pytz.timezone("Asia/Tokyo")))

#CheckLimitResultクラスのstateの値を表わすenum型
class CheckLimitResultState(IntEnum):
    SUCCEEDED = auto()
    ERROR = auto()

#リミットステータスの戻り値
class CheckLimitResult:
    limit = 0       #最大リミット数
    remaining = 0   #残りの回数
    resetTime = 0       #次にリセットされる時間
    state = CheckLimitResultState.ERROR

    #コンストラクタ
    def __init__(self, limit, remaining, resetTime, state):
        self.limit = limit
        self.remaining = remaining
        self.resetTime = resetTime
        self.state = state
        
def consumeLimit( user_id, status_name, limitMax, interval_minute):
    '''
    リミットステータスを消費する

    user_id(String): ユーザーID
    status_name(String): ステータス名
    limitMax(timedelta): 時間をリセットする時間の間隔
    interval_minute(int): リミットステータスが回復するまでの時間（分）

    ■参考
        ツイッターリミット数: https://developer.x.com/ja/docs/x-api/rate-limits
    '''
    try:
        #現在の時刻を取得する
        now = datetime.datetime.now()

        #直近でリミットを補充できた時間を取得する
        latestRecoveryTime = now.replace(minute= now.minute - now.minute % interval_minute, second=0, microsecond=0)

        #リミットステータスが入ったレコードを取得する
        rateLimitStatus = g.db.session.query(RateLimitStatus).filter(
                and_(
                    RateLimitStatus.user_id == user_id,
                    RateLimitStatus.status_name == status_name
                )
            ).first()

        #まだ要素が存在していなけば要素を新規作成する
        if rateLimitStatus == None:
            rateLimitStatus = RateLimitStatus()
            rateLimitStatus.user_id = user_id
            rateLimitStatus.status_name = status_name
            rateLimitStatus.remaining = limitMax
            rateLimitStatus.latest_reset_time = now

        #直近のリミットを補充した時間より、前回補充した時間が前だったら、リミットをリセットする
        if rateLimitStatus.latest_reset_time < latestRecoveryTime:
            rateLimitStatus.remaining = limitMax
            rateLimitStatus.latest_reset_time = now

        #まだ上限に達していなければリミットステータスをデクリメントしてデータベースを更新する
        if rateLimitStatus.remaining > 0:
            rateLimitStatus.remaining -= 1
            
            #要素を追加または更新する
            g.db.session.add(rateLimitStatus)
            
            #結果を取得する
            result = CheckLimitResultState.SUCCEEDED
        else:
            #結果を取得する
            result = CheckLimitResultState.ERROR

        #コミット
        # TODO このコミットは本当に必要か、後で確認する事
        g.db.session.commit()

        print(
            ""
            + "リミットステータスを更新しました"
            + "\n\tステータス名: " + status_name
            + "\n\t最後にリセットされた日時: " + latestRecoveryTime.strftime('%Y年%m月%d日 %H時間%M分%S秒')
        )

        return CheckLimitResult(
            limitMax,
            rateLimitStatus.remaining,
            now.replace(minute= now.minute + interval_minute - now.minute % interval_minute, second=0, microsecond=0),
            result
        )
    
    except Exception as e:
        return None



#その他--------------------------------------------------------

class Info(Base, g.db.Model):
    __tablename__ = 'info'
    info_id = g.db.Column( g.db.Integer, primary_key=True, autoincrement=True, default=0)
    next_media_id =  g.db.Column( g.db.Integer, nullable=False, default=0)

#時刻関連--------------------------------------------------------

def strToDate(str):
    now_datetime = datetime.datetime.strptime( str, '%Y/%m/%d %H:%M:%S')
    tdate = datetime.datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
    
    return tdate


#スケルトンプログラム--------------------------------------------------------
@app.route('/api/1.0/skeleton/<q>', methods=['GET'])
def skeleton(q):
    """
    スケルトンプログラム

    Query parameters:
        q(String): 検索する文字列

    JSON body parameters:
        Authorization(String): ユーザーを認証するためのトークン

    Raises:
        Exception: _description_

    Returns:
        String: 結果を表わすJSON
    """
    if request.method == 'GET':
        try:
            #ログイン中のユーザーのIDを取得する
            userId = getUser()["user_id"]

            #ログインされていなければ例外を発生させる
            if userId == None:
                Exception("ユーザーがログインしていません。")

            #DBからデータを取得する
            dbEvents = g.db.session.query(Event)
            dbEvents = dbEvents.filter(
                    or_(
                        Event.title.like(f'%{q}%'),
                        Event.overview.like(f'%{q}%'),
                        )
                    ).all()
            
            g.db.session.commit()

            json = {
                "data": []
            }

            for event in dbEvents:
                json["data"].append(event.title)

            return make_response(
                    jsonify(
                            json,
                        )
                    )
        except Exception as e:
            return make_response(
                    jsonify(
                            {
                                "status": "error",
                                "message": e
                            }
                        )
                    )


#--------------------------------------------------------

@app.route('/')
def index():
    return render_template(
        'index.html'
    )


#Like関連--------------------------------------------------------

@app.route('/api/1.0/users/<user_id>/likes', methods=['POST'])
def postLikesEvent(user_id):
    """
    イベントをLike状態にする
    
    パスパラメータ
        user_id: likeするユーザーのID
        
    JSONパラメータ
        event_id: likeするイベントのID
    """
    
    #Likeイベントテーブルを更新する
    try:
        #Likeが既に登録されているか確認する
        likeEvent = g.db.session.query(LikeEvent).filter(
                and_(
                    LikeEvent.user_id == user_id,
                    LikeEvent.event_id == request.json["event_id"]
                )
            ).first()
        
        #Likeが登録されていなければ登録する
        if likeEvent == None:
            likeEvent = LikeEvent(
                user_id = user_id,
                event_id = int(request.json["event_id"]),
            )
            g.db.session.add(likeEvent)
            g.db.session.commit()
        
        return '''
{
  "data": {
    "liked": true
  }
}
'''

    except Exception as e:
        return '''
{
    "status": "Error",
    "message": "更新に失敗しました。"
}
'''

@app.route('/api/1.0/users/<user_id>/likes/<event_id>', methods=['DELETE'])
def deleteLikesEvent(user_id, event_id):
    try:
        g.db.session.query(LikeEvent). \
        filter(
            and_(
                LikeEvent.user_id == user_id,
                LikeEvent.event_id == event_id
                )
        ).delete()
        
        g.db.session.commit()
    
        return make_response('''
{
  "data": {
    "liked": false
  }
}
''')

    except Exception as e:
        return make_response('''
{
    "status": "Error",
    "message": "更新に失敗しました。"
}
''')

@app.route('/api/1.0/users/<user_id>/liked_events', methods=['GET'])
def getLikedEvent(user_id):
    '''
    特定のユーザーが任意のイベントにLikeしているかを調べる
    ※このメソッドはTwitterのAPIにはありません。
    '''
    dbLikeEvents = g.db.session.query(LikeEvent). \
        filter(
            and_(
                LikeEvent.user_id == user_id,
                LikeEvent.event_id == event_id
                )
        ).all()
    g.db.session.commit()

    for likeEvent in dbLikeEvents:
        return make_response('''
{
  "data": {
    "liked": true
  }
}
''')
    
    return make_response('''
{
  "data": {
    "liked": false
  }
}
''')

@app.route('/api/1.0/users/<user_id>/liked_events', methods=['POST'])
def postLikedEvents(user_id):
    
    """
    ユーザーが「like」したイベントに関する情報を取得できます。

    パスパラメータ
        user_id: likeをした人のID
        
    JSONパラメータ
        event_ids ([]): 絞り込みに使うイベントIDのリスト

    """

    #Likeイベントテーブルを取得する
    try:
        event_ids = request.json["event_ids"] #値が存在するかを確認する

        dbLikeEvents = g.db.session.query(LikeEvent)
        
        #ユーザーで絞り込みをする
        dbLikeEvents = dbLikeEvents.filter(LikeEvent.user_id == str(user_id))
        
        #イベントで絞り込みをする
        orArg = []
        for event_id in event_ids:
            orArg.append(LikeEvent.event_id == event_id["event_id"])
        dbLikeEvents = dbLikeEvents.filter(
                        or_(*orArg)
                    )
        
        #DBからデータを取得する
        dbLikeEvents.all()
        g.db.session.commit()
        
        #返却するデータを作成する
        data = []
        for likeEvent in dbLikeEvents:
            data.append(
                    {
                        "event_id": likeEvent.event_id,
                    }
                )
        return make_response(f'''
{{
    "status": "OK",
    "message": "更新に成功しました。",
    "data": {data}
}}
''')

    except Exception as e:
        return make_response('''
{
    "status": "Error",
    "message": "更新に失敗しました。"
}
''')


#ユーザー関連--------------------------------------------------------

@app.route('/api/1.0/users/', methods=['POST'])
def postUser():
    '''
    ユーザーを登録、または更新する
    '''
    try:
        userId = getUser()["user_id"]

        user = None

        #ユーザー情報の更新
        try:
            request.json["username"]    #usernameが渡されていれば更新
        
            #DBからユーザーの情報を取得する
            user = g.db.session.query(User).filter(User.user_id == userId).first()

            #取得に失敗した場合エラーを返す
            if user == None:
                return make_response(
                    jsonify(
                            {
                                "state": "error"
                            },
                        )
                    )

            #ユーザー情報を更新する
            user.name = normalizeValue(request.json, "name") if normalizeValue(request.json, "name") != None else ""
            user.username = normalizeValue(request.json, "username") if normalizeValue(request.json, "username") != None else ""
            user.profile_media_id = normalizeValue(request.json, "profile_media_id")
            user.biography = normalizeValue(request.json, "biography") if normalizeValue(request.json, "biography") != None else ""
            user.website = normalizeValue(request.json, "website") if normalizeValue(request.json, "website") != None else ""

            g.db.session.commit()

            return make_response(
                jsonify(
                        {
                            "state": "ok"
                        },
                    )
                )

        except Exception as e:
            pass

        #ユーザー情報の新規作成
        try:
            #ユーザーネームを新規作成する
            tempUserName = None
            for i in range(1000):    #最大1000回usernameの作成を試す
                shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyz0123456789_")
                tempUserName = "$" + shortuuid.uuid()

                #DBに同じユーザーネームが登録されていないか確認する
                user = g.db.session.query(User).filter(User.username == tempUserName).first()
                
                if user == None:
                    break

            #既にusernameが存在していればエラーを返す
            if user != None:
                return make_response(
                    jsonify(
                            {
                                "state": "error",
                                "message": "ユーザー名の作成に失敗しました。"
                            },
                        )
                    )

            #ユーザーデータを作成する
            user = User()
            user.user_id = userId
            user.name = "New User"
            user.username = tempUserName
            user.profile_media_id = None
            user.biography = ""
            user.website = ""

            #ユーザーデータを登録する
            g.db.session.add(user)

            #ブックマークグループを作成する
            _postBookmarkGroup( "art_event", "後で観る")
            _postBookmarkGroup( "art_event", "行きたい")
            _postBookmarkGroup( "art_event", "行った")

            _postBookmarkGroup( "user_list", "フォロー")

        except Exception as e:
            return make_response(
                jsonify(
                        {
                            "state": "error"
                        },
                    )
                )

        #コミットする
        g.db.session.commit()

        return make_response(
            jsonify(
                    {
                        "state": "ok"
                    },
                )
            )
    
    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "state": "ok",
                        "message": e
                    }
                )
            )

@app.route('/api/1.0/users/user_id/<username>', methods=['GET'])
def getUserIdFromUsername(username):
    '''
    スクリーンネームからユーザーIDを取得する

    プログラム内から直接呼び出された場合はjsonではなく、ユーザーIDを直接返す
    '''
    try:
        #ユーザーネームからユーザーを検索する
        user = g.db.session.query(User).filter(
                User.username == username,
            ).first()
    
        #コミットする
        g.db.session.commit()

        #GETメソッドだった場合、jsonを返す
        if request.method == 'GET':
            return make_response(
                jsonify(
                        {
                            "data": {
                                "user_id": user.user_id
                            }
                        },
                        
                        
                    )
                )
        
        #メソッドがプログラム内から直接呼び出された場合、IDの値をそのまま返す
        return user.user_id

    except Exception as e:
        return make_response(
                jsonify(
                    {
                        "state": "error"
                    },
                )
            )
    
@app.route('/api/1.0/users/<user_id>', methods=['GET'])
def getUsers(user_id):
    '''
    ユーザーIDからユーザーの情報を取得する
    '''
    try:
        #ユーザーIDからユーザーの情報を取得する
        dbUser = g.db.session.query(User).filter(
                User.user_id == user_id,
            ).first()
        
        #メタデータを取得する
        dbMetaList = g.db.session.query(Usermeta).filter(
                Usermeta.user_id == user_id,
            ).all()
        
        #
        g.db.session.commit()

        #ユーザーが存在しなければエラーを返す
        if dbUser == None:
            raise Exception("ユーザー情報の取得に失敗しました。")

        #メタデータをJsonに変換する
        user = UserSchema().dump(dbUser)


        #メタデータをJsonに変換する
        metaList = UsermetaSchema(
                many=True,
            ).dump(dbMetaList)
        
        #ユーザ情報にメタ情報を挿入する
        user["meta"] = metaList

        #権限を取得する
        roles = getAllUserRoles(dbUser.user_role_group_id)
        user["role_group_name"] = roles["role_group_name"]
        user["roles"] = roles["roles"]

        #TODO
        user["public_metrics"] = {}
        user["public_metrics"]["follow"] = 0
        user["public_metrics"]["follower"] = 0

        #プロフィール画像のURLを追加する
        try:
            if dbUser.profile_media_id != None:
                user["profile_media_id"] = dbUser.profile_media_id
            else:
                user["profile_media_id"] = None
        except Exception as e:
            pass
        
        return make_response(
            jsonify(
                    {
                        "data": user
                    },
                    
                    
                )
            )

    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "status": "error"
                    },
                    
                    
                )
            )

@app.route("/api/1.0/users/search/all", methods=["POST"])
def getUsersSearchAll():
    '''
    リストに登録されたユーザーのリストを取得する

    JSON body parameters:
        bookmark_group_id(String?): ブックマークのID
    '''
    try:
        bookmark_group_ids = None

        dbRes = dbRes = g.db.session.query(BookmarkStr)

        #ブックマークIDで絞り込む
        if "bookmark_group_id" in request.json:
            bookmark_group_id = request.json["bookmark_group_id"]

            dbRes = g.db.session.query(BookmarkStr).filter(
                and_(
                    BookmarkGroupStr.type == "user_list",
                    BookmarkStr.bookmark_group_id == request.json["bookmark_group_id"]
                )
            )

        if "bookmark_group_id" in request.json:
            dbRes.join(
                BookmarkGroupStr,
                BookmarkGroupStr.bookmark_group_id == BookmarkStr.bookmark_group_id,
                isouter = True
        )
        
        dbRes.all()

        g.db.session.commit()

        res = []
        for bookmark in dbRes:
            res.append(
                {
                    "user_id": bookmark.target_id,
                    "memo": bookmark.memo
                }
            )
        return make_response(
            jsonify(
                {
                    "status": "ok",
                    "data": res
                }
            )
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error"
                }
            )
        )


#フォロー関連----------------------------------------------------

@app.route("/api/1.0/users/follow", methods=["POST"])
def getUsersFollow():
    '''
    特定のユーザーがフォローされているか調べる
    '''
    try:
        res = False

        userId = getUser()["user_id"]

        dbRes = g.db.session.query(BookmarkStr)

        dbRes = dbRes.filter(
            and_(
                BookmarkGroupStr.type == "user_list",
                BookmarkGroupStr.name == "フォロー",
                BookmarkGroupStr.user_id == userId,
                BookmarkStr.target_id == request.json["user_id"],
            )
        ).join(
            BookmarkGroupStr,
            BookmarkGroupStr.bookmark_group_id == BookmarkStr.bookmark_group_id,
            isouter = True
        ).first()

        g.db.session.commit()

        if dbRes != None:
            res = True

        return make_response(
            jsonify(
                {
                    "data": res,
                }
            )
        )

    except Exception as e:
        print(e)
        return make_response(
            jsonify(
                {
                    "state": "error",
                }
            )
        )
    


#ユーザーメタ関連----------------------------------------------------------

@app.route("/usermeta/add", methods=["POST"])
def postUserMetadata():
    '''
    ユーザーメタデータに要素を追加する

    JSON body parameters:
        overwrite(bool): trueにすると上書き
        meta_type(String): メタデータのタイプ
        meta_key(String): メタデータのキー
        meta_value(String): メタデータの値
    '''
    try:
        userId = None

        #ユーザーIDの取得を試みる
        try:
            userId = getUser()["user_id"]
        except Exception as e:
            pass

        #リリース時、ログインしていなければ例外を発生する
        if g.isDebug() == False:
            if userId == None:
                raise Exception("ユーザーがログインしていません")
        #デバッグ時、ログインしているユーザーが居なければID1のユーザーをログイン中とする
        else:
            if userId == None:
                userId = 1
        
        overwrite = False

        #上書き指定を取得する
        if "overwrite" in request.json:
            overwrite = request.json["overwrite"]


        #上書き指定されていた場合、既存のデータを削除する
        if overwrite == True:
            deleteUserMetadata(
                userId,
                request.json["meta_key"]
            )

        #新規にメタデータを挿入する
        metadata = Usermeta()
        metadata.user_id = userId
        metadata.meta_type = request.json["meta_type"]
        metadata.meta_key = request.json["meta_key"]
        metadata.meta_value = request.json["meta_value"]

        g.db.session.add(metadata)

        g.db.session.commit()

        return make_response(
                jsonify(
                        {
                            "status": "OK",
                        },
                    )
                )

    except Exception as e:
        g.db.session.rollback()
        return make_response(
                jsonify(
                        {
                            "status": "error",
                        },
                    )
                )
    
@app.route("/usermeta/get", methods=["POST"])
def getUserMetadata():
    '''
    ユーザーメタデータを取得

    JSON body parameters:
        meta_key(String): メタデータのキー
    '''
    try:
        userId = None

        #ユーザーIDの取得を試みる
        try:
            userId = getUser()["user_id"]
        except Exception as e:
            pass

        #リリース時、ログインしていなければ例外を発生する
        if g.isDebug() == False:
            if userId == None:
                raise Exception("ユーザーがログインしていません")
        #デバッグ時、ログインしているユーザーが居なければID1のユーザーをログイン中とする
        else:
            if userId == None:
                userId = 1
        
        #検索条件を作成する
        andArg = []
        andArg.append(Usermeta.user_id == userId)
        if "meta_type" in request.json:
            andArg.append(Usermeta.meta_type == request.json["meta_type"])
        if "meta_key" in request.json:
            andArg.append(Usermeta.meta_key == request.json["meta_key"])
        if "meta_value" in request.json:
            andArg.append(Usermeta.meta_value == request.json["meta_value"])
        dbUsermetaList = g.db.session.query(Usermeta).filter(
            and_(
                *andArg
            )
        ).all()

        #メタデータをJsonに変換する
        usermetaList = UsermetaSchema(
                many=True,
            ).dump(dbUsermetaList)

        return make_response(
                jsonify(
                        {
                            "status": "OK",
                            "data": {
                                "usermeta_list": usermetaList
                            }
                        },
                    )
                )

    except Exception as e:
        g.db.session.rollback()
        return make_response(
                jsonify(
                        {
                            "status": "error",
                        },
                    )
                )


@app.route("/usermeta/delete", methods=["POST"])
def DeleteUserMetadata():
    '''
    メタデータを削除する

    JSON body parameters:
        meta_key(String): メタデータのキー
    '''
    try:
        userId = None
        
        #ユーザーIDの取得を試みる
        try:
            userId = getUser()["user_id"]
        except Exception as e:
            pass

        #リリース時、ログインしていなければ例外を発生する
        if g.isDebug() == False:
            if userId == None:
                raise Exception("ユーザーがログインしていません")
        #デバッグ時、ログインしているユーザーが居なければID1のユーザーをログイン中とする
        else:
            if userId == None:
                userId = 1
        
        deleteUserMetadata(
            userId,
            request.json["meta_key"],
        )

        g.db.session.commit()

        return make_response(
                jsonify(
                        {
                            "status": "OK",
                        },
                    )
                )

    except Exception as e:
        return make_response(
                jsonify(
                        {
                            "status": "error",
                        },
                    )
                )

def deleteUserMetadata( user_id, metaa_key):
    try:
        g.db.session.query(Usermeta).filter(
            and_(
                Usermeta.user_id == user_id,
                Usermeta.meta_key == metaa_key,
            )
        ).delete()

    except Exception as e:
        raise e
    

#ユーザー権限関連--------------------------------------------------------

def getAllUserRoles(user_role_group_id):
    '''
    ユーザーグループの全ての権限を取得する

    user_role_group_id(String): ユーザーグループID
    '''
    try:
        userRoleGroup = g.db.session.query(UserRoleGroup).filter(UserRoleGroup.user_role_group_id == user_role_group_id).first()
        if(userRoleGroup == None):
            raise Exception("ユーザー権限グループが見つかりません。")

        userRoles = g.db.session.query(UserRole).filter(UserRole.user_role_group_id == userRoleGroup.user_role_group_id).all()

        j = {
            "role_group_name": userRoleGroup.role_group_name,
            "roles": []
        }

        for role in userRoles:
            j["roles"].append(role.value)

        return j

    except Exception as e:
        raise e


#ブックマーク関連--------------------------------------------------------

@app.route('/api/1.0/bookmarks/', methods=['POST'])
def postBookmarkGroup():
    """
    ブックマークグループを作成する
    
    パスパラメータ
        なし
        
    JSONパラメータ
        name: 作成するブックマークグループの名前
    """
    try:
        bookmarkGropu = _postBookmarkGroup(request.json["type"], request.json["name"])

        g.db.session.commit()

        return make_response(
            jsonify(
                {
                    "data": {
                        "id": bookmarkGropu.bookmark_group_id,
                        "name": bookmarkGropu.name
                    }
                }
            )
        )

    except Exception as e:
        return make_response(
                    jsonify(
                            {
                                "state": "error"
                            },
                        )
                    )

def _postBookmarkGroup( type, name):
    #ユーザーIDを取得する
    userId = getUser()["user_id"]

    #同じ名前のブックマークグループ既に登録されているか確認する
    bookmarkGroups = g.db.session.query(BookmarkGroup).filter(
        and_(
            BookmarkGroup.user_id == userId,
            BookmarkGroup.type == type,
            BookmarkGroup.name == name
        )
    ).all()

    if len(bookmarkGroups) > 0:
        raise Exception("ブックマークグループ" + name + "は既に存在しています。")

    #ブックマークグループを作成
    bookmarkGropu = BookmarkGroup()
    bookmarkGropu.user_id = userId
    bookmarkGropu.type = type
    bookmarkGropu.name = name

    #ブックマークグループをDBに登録
    g.db.session.add(bookmarkGropu)

    return bookmarkGropu
    
                
@app.route('/api/1.0/bookmark_group/<bookmark_group_id>', methods=['DELETE'])
def deleteBookmarkGroup(bookmark_group_id):
    """
    ブックマークグループを削除する
    
    パスパラメータ
        bookmark_gropu_id: ブックマークグループのID
        
    JSONパラメータ
        user_id: ブックマークを削除するユーザーのID
                 このパラメータは将来的に廃止し、OAuth認証を使うこと
    """
    try:
        #ユーザーIDを取得する
        userId = getUser()["user_id"]

        #ブックマークを削除する
        bookmarkGroupList =  g.db.session.query(Bookmark).filter(
            and_(
                Bookmark.user_id == userId,
                Bookmark.bookmark_group_id == bookmark_group_id
                )
        ).delete()

        #ブックマークグループを削除する
        bookmarkGroupList =  g.db.session.query(BookmarkGroup).filter(
            and_(
                BookmarkGroup.user_id == userId,
                BookmarkGroup.bookmark_group_id == bookmark_group_id
                )
        ).delete()

        g.db.session.commit()
    
        return make_response(f'''
{{
    "data": {{
        "deleted": true
    }}
}}
''')
    
    except Exception as e:
        g.db.session.rollback()
        
        return make_response(f'''
{{
    "data": {{
        "deleted": false
    }}
}}
''')


@app.route('/api/1.0/bookmark_group_name/<bookmark_group_id>', methods=['PUT'])
def updateBookmarkGroupName(bookmark_group_id):
    """
    ブックマークグループ名を変更する
    
    パスパラメータ
        bookmark_gropu_id: ブックマークグループのID
        
    JSONパラメータ
        user_id: ブックマークを削除するユーザーのID
                 このパラメータは将来的に廃止し、OAuth認証を使うこと
        name: 作成するブックマークグループの名前
    """
    try:
        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ブックマークグループ既に登録されているか確認する
        bookmarkGroups = g.db.session.query(BookmarkGroup).filter(
            and_(
                BookmarkGroup.user_id == userId,
                BookmarkGroup.type == request.json["type"],
                BookmarkGroup.name == request.json["name"]
            )
        ).all()

        if len(bookmarkGroups) > 0:
            raise Exception("ブックマークグループ Type: " + request.json["type"] + ", Name: " + request.json["name"] + "は既に存在しています。")
        
        #ブックマークグループ名を変更する
        bookmarkGroup = g.db.session.query(BookmarkGroup). \
        filter(
            and_(
                BookmarkGroup.user_id == userId,
                BookmarkGroup.bookmark_group_id == bookmark_group_id
                )
        ).first()

        #ブックマーク名を変更する
        bookmarkGroup.name = request.json["name"]

        #コミットする
        g.db.session.commit()
    
        return make_response(f'''
{{
    "data": {{
        "deleted": true
    }}
}}
''')
    
    except Exception as e:
        return make_response(f'''
{{
    "data": {{
        "deleted": false
    }}
}}
''')

@app.route('/api/1.0/get_bookmarks_containing_event/', methods=['GET'])
def getBookmarksContainingEvent():
    """
    指定されたターゲットIDが入っているブックマークのリストを全て取得する
    
    パスパラメータ
        user_id: 取得するリストを所有するユーザー ID。
        
    JSONパラメータ
        なし
    """
    try:
        res = []

        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ログインされていなければ例外を発生させる
        if userId == None:
            Exception("ユーザーがログインしていません。")

        #イベントが入ったブックマークを全て取得する
        bookmarks = g.db.session.query(Bookmark).filter(
            and_(
                Bookmark.user_id == userId,
                BookmarkGroup.type == request.headers.get("Type", None),
                Bookmark.target_id == request.headers.get("Target-Id", None),
            )
        ).join(
            BookmarkGroup,
            Bookmark.bookmark_group_id == BookmarkGroup.bookmark_group_id
        ).all()

        g.db.session.commit()

        #結果を配列に格納する
        for bookmark in bookmarks:
            res.append(bookmark.bookmark_group_id)

        j = {
            "data": []
        }

        j["data"] = res

        return make_response(
                jsonify(
                        j,
                    )
                )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                )
            )

@app.route('/api/1.0/users/<user_id>/owned_bookmarks/', methods=['GET'])
def getUsersBookmarks(user_id):
    """
    指定されたユーザーが所有するすべてのリストを返します。
    パスパラメータ
        user_id: 取得するリストを所有するユーザー ID。
        
    JSONパラメータ
        なし
    """
    try:
        bookmarkGroups = g.db.session.query(BookmarkGroup).filter(
            BookmarkGroup.user_id == user_id,
            BookmarkGroup.type == request.headers["type"]
        ).all()

        res = {
            "data": []
        }

        for bookmarkGroup in bookmarkGroups:
            res["data"].append(
                {
                    "bookmark_group_id": bookmarkGroup.bookmark_group_id,
                    "name": bookmarkGroup.name,
                }
            )

        return make_response(
            jsonify(
                    res,
                )
            )
    
    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "state": "error"
                    }
                )
            )

@app.route('/api/1.0/users/<user_id>/bookmarks/', methods=['POST'])
def postBookmark(user_id):

    """
    イベントをブックマークする
    
    パスパラメータ
        user_id: likeするユーザーのID
        
    JSONパラメータ
        target_id: likeするイベントやユーザーなどのID
        bookmark_group_id: ブックマークグループのID
        bookmark_group_name: ブックマークグループ名
    """
    
    #ブックマークテーブルを更新する
    try:
        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ログインされていなければ例外を発生させる
        if userId == None:
            Exception("ユーザーがログインしていません。")
            
        #ブックマークが既に登録されているか確認する
        bookmark = g.db.session.query(Bookmark).filter(
                and_(
                    Bookmark.bookmark_group_id == request.json["bookmark_group_id"],
                    Bookmark.user_id == userId,
                    Bookmark.target_id == request.json["target_id"],
                )
            ).first()
        
        #ブックマークが登録されていなければ登録する
        if bookmark == None:
            bookmark = Bookmark()
            bookmark.bookmark_group_id = request.json["bookmark_group_id"]
            bookmark.user_id = userId
            bookmark.target_id = int(request.json["target_id"])

            g.db.session.add(bookmark)

        #コミットする
        g.db.session.commit()
        
        return '''
{
  "data": {
    "bookmarked": true
  }
}
'''

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                
                
                )
            )


@app.route('/api/1.0/users/<user_id>/bookmarks/<bookmark_group_id>/<target_id>', methods=['DELETE'])
def deleteBookmark(user_id, bookmark_group_id, target_id):

    """
    イベントのブックマークを解除する
    
    パスパラメータ
        user_id: ブックマークを削除するユーザーのID
        
    JSONパラメータ
        event_id: ブックマークするイベントのID
        bookmark_group_id: ブックマークグループのID
    """
    
    try:
        userId = getUser()["user_id"]

        g.db.session.query(Bookmark). \
        filter(
            and_(
                Bookmark.bookmark_group_id == bookmark_group_id,
                Bookmark.user_id == userId,
                Bookmark.target_id == target_id,
                )
        ).delete()
        
        g.db.session.commit()
    
        return make_response('''
{
  "data": {
    "bookmarked": false
  }
}
''')

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                
                
                )
            )



#ブックマーク関連(ターゲットがString型バージョン)--------------------------------------------------------


@app.route('/api/1.0/bookmarks_str/', methods=['POST'])
def postBookmarkGroupStr():
    """
    ブックマークグループを作成する
    
    パスパラメータ
        なし
        
    JSONパラメータ
        name: 作成するブックマークグループの名前
    """
    try:
        bookmarkGropu = _postBookmarkGroup_str(request.json["type"], request.json["name"])

        g.db.session.commit()

        return make_response(
            jsonify(
                {
                    "data": {
                        "id": bookmarkGropu.bookmark_group_id,
                        "name": bookmarkGropu.name
                    }
                }
            )
        )

    
    except Exception as e:
        return make_response(
                    jsonify(
                            {
                                "state": "error"
                            },
                        )
                    )

def _postBookmarkGroup_str( type, name):
    #ユーザーIDを取得する
    userId = getUser()["user_id"]

    #同じ名前のブックマークグループ既に登録されているか確認する
    bookmarkGroups = g.db.session.query(BookmarkGroupStr).filter(
        and_(
            BookmarkGroupStr.user_id == userId,
            BookmarkGroupStr.type == type,
            BookmarkGroupStr.name == name
        )
    ).all()

    if len(bookmarkGroups) > 0:
        raise Exception("ブックマークグループ" + name + "は既に存在しています。")

    #ブックマークグループを作成
    bookmarkGropu = BookmarkGroupStr()
    bookmarkGropu.user_id = userId
    bookmarkGropu.type = type
    bookmarkGropu.name = name

    #ブックマークグループをDBに登録
    g.db.session.add(bookmarkGropu)

    return bookmarkGropu
    
                
@app.route('/api/1.0/bookmark_group_str/<bookmark_group_id>', methods=['DELETE'])
def deleteBookmarkGroup_str(bookmark_group_id):
    """
    ブックマークグループを削除する
    
    パスパラメータ
        bookmark_gropu_id: ブックマークグループのID
        
    JSONパラメータ
        user_id: ブックマークを削除するユーザーのID
                 このパラメータは将来的に廃止し、OAuth認証を使うこと
    """
    try:
        #ユーザーIDを取得する
        userId = getUser()["user_id"]

        #ブックマークを削除する
        bookmarkGroupList =  g.db.session.query(BookmarkStr).filter(
            and_(
                BookmarkStr.user_id == userId,
                BookmarkStr.bookmark_group_id == bookmark_group_id
                )
        ).delete()

        #ブックマークグループを削除する
        bookmarkGroupList =  g.db.session.query(BookmarkGroupStr).filter(
            and_(
                BookmarkGroupStr.user_id == userId,
                BookmarkGroupStr.bookmark_group_id == bookmark_group_id
                )
        ).delete()

        g.db.session.commit()
    
        return make_response(f'''
{{
    "data": {{
        "deleted": true
    }}
}}
''')
    
    except Exception as e:
        g.db.session.rollback()
        
        return make_response(f'''
{{
    "data": {{
        "deleted": false
    }}
}}
''')


@app.route('/api/1.0/bookmark_group_name_str/<bookmark_group_id_str>', methods=['PUT'])
def updateBookmarkGroupName_str(bookmark_group_id):
    """
    ブックマークグループ名を変更する
    
    パスパラメータ
        bookmark_gropu_id: ブックマークグループのID
        
    JSONパラメータ
        user_id: ブックマークを削除するユーザーのID
                 このパラメータは将来的に廃止し、OAuth認証を使うこと
        name: 作成するブックマークグループの名前
    """
    try:
        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ブックマークグループ既に登録されているか確認する
        bookmarkGroups = g.db.session.query(BookmarkGroupStr).filter(
            and_(
                BookmarkGroupStr.user_id == userId,
                BookmarkGroupStr.type == request.json["type"],
                BookmarkGroupStr.name == request.json["name"]
            )
        ).all()

        if len(bookmarkGroups) > 0:
            raise Exception("ブックマークグループ Type: " + request.json["type"] + ", Name: " + request.json["name"] + "は既に存在しています。")
        
        #ブックマークグループ名を変更する
        bookmarkGroupStr = g.db.session.query(BookmarkGroupStr). \
        filter(
            and_(
                BookmarkGroupStr.user_id == userId,
                BookmarkGroupStr.bookmark_group_id == bookmark_group_id
                )
        ).first()

        #ブックマーク名を変更する
        bookmarkGroupStr.name = request.json["name"]

        #コミットする
        g.db.session.commit()
    
        return make_response(f'''
{{
    "data": {{
        "deleted": true
    }}
}}
''')
    
    except Exception as e:
        return make_response(f'''
{{
    "data": {{
        "deleted": false
    }}
}}
''')

@app.route('/api/1.0/get_bookmarks_containing_event_str/', methods=['GET'])
def getBookmarksContainingEvent_str():
    """
    指定されたターゲットIDが入っているブックマークのリストを全て取得する
    
    パスパラメータ
        user_id: 取得するリストを所有するユーザー ID。
        
    JSONパラメータ
        なし
    """
    try:
        res = []

        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ログインされていなければ例外を発生させる
        if userId == None:
            Exception("ユーザーがログインしていません。")

        #イベントが入ったブックマークを全て取得する
        bookmarks = g.db.session.query(BookmarkStr).filter(
            and_(
                BookmarkStr.user_id == userId,
                BookmarkGroupStr.type == request.headers.get("Type", None),
                BookmarkStr.target_id == request.headers.get("Target-Id", None),
            )
        ).join(
            BookmarkGroupStr,
            BookmarkStr.bookmark_group_id == BookmarkGroupStr.bookmark_group_id
        ).all()

        g.db.session.commit()

        #結果を配列に格納する
        for bookmark in bookmarks:
            res.append(bookmark.bookmark_group_id)

        j = {
            "data": []
        }

        j["data"] = res

        return make_response(
                jsonify(
                        j,
                    )
                )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                )
            )

@app.route('/api/1.0/users/<user_id>/owned_bookmarks_str/', methods=['GET'])
def getUsersBookmarks_str(user_id):
    """
    指定されたユーザーが所有するすべてのリストを返します。
    パスパラメータ
        user_id: 取得するリストを所有するユーザー ID。
        
    JSONパラメータ
        なし
    """
    try:
        bookmarkGroups = g.db.session.query(BookmarkGroupStr).filter(
            BookmarkGroupStr.user_id == user_id,
            BookmarkGroupStr.type == request.headers["type"]
        ).all()

        res = {
            "data": []
        }

        for bookmarkGroup in bookmarkGroups:
            res["data"].append(
                {
                    "bookmark_group_id": bookmarkGroup.bookmark_group_id,
                    "name": bookmarkGroup.name,
                }
            )

        return make_response(
            jsonify(
                    res,
                )
            )
    
    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "state": "error"
                    }
                )
            )

@app.route('/api/1.0/users/<user_id>/bookmarks_str/', methods=['POST'])
def postBookmark_str(user_id):

    """
    イベントをブックマークする
    
    パスパラメータ
        user_id: likeするユーザーのID
        
    JSONパラメータ
        target_id: likeするイベントやユーザーなどのID
        bookmark_group_id: ブックマークグループのID
        bookmark_group_name: ブックマークグループ名
    """
    
    #ブックマークテーブルを更新する
    try:
        #ログイン中のユーザーのIDを取得する
        userId = getUser()["user_id"]

        #ログインされていなければ例外を発生させる
        if userId == None:
            Exception("ユーザーがログインしていません。")
            
        #ブックマークが既に登録されているか確認する
        bookmark = g.db.session.query(BookmarkStr).filter(
                and_(
                    BookmarkStr.bookmark_group_id == request.json["bookmark_group_id"],
                    BookmarkStr.user_id == userId,
                    BookmarkStr.target_id == request.json["target_id"],
                )
            ).first()
        
        #ブックマークが登録されていなければ登録する
        if bookmark == None:
            bookmark = BookmarkStr()
            bookmark.bookmark_group_id = request.json["bookmark_group_id"]
            bookmark.user_id = userId
            bookmark.target_id = request.json["target_id"]

            g.db.session.add(bookmark)

        #コミットする
        g.db.session.commit()
        
        return '''
{
  "data": {
    "bookmarked": true
  }
}
'''

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                
                
                )
            )


@app.route('/api/1.0/users/<user_id>/bookmarks_str/<bookmark_group_id>/<target_id>', methods=['DELETE'])
def deleteBookmark_str(user_id, bookmark_group_id, target_id):

    """
    イベントのブックマークを解除する
    
    パスパラメータ
        user_id: ブックマークを削除するユーザーのID
        
    JSONパラメータ
        event_id: ブックマークするイベントのID
        bookmark_group_id: ブックマークグループのID
    """
    
    try:
        userId = getUser()["user_id"]

        g.db.session.query(BookmarkStr). \
        filter(
            and_(
                BookmarkStr.bookmark_group_id == bookmark_group_id,
                BookmarkStr.user_id == userId,
                BookmarkStr.target_id == target_id,
                )
        ).delete()
        
        g.db.session.commit()
    
        return make_response('''
{
  "data": {
    "bookmarked": false
  }
}
''')

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                
                
                )
            )



#メディア関連--------------------------------------------------------

@app.route('/api/1.0/media/register', methods=['POST'])
def postMedia():
    """
    ☆
    予めアップロードしたメディアの情報を追加する。
    ■リクエストボディーの例
    {
        "media_id": 12345,
        "content_type": "image/jpg"
    }

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        try:
            userId = getUser()["user_id"]

            #まず、本当にファイルがアップロードされているかを確認する
            #Firebaseを初期化する（環境変数を使っている場合）
            firebase_admin.initialize_app()
            
            #フォルダを取得する
            error = True
            bucket = storage.bucket("gallery-log-859ae.appspot.com")
            blobs = bucket.list_blobs("media")
            for blob in blobs:
                if(blobs.name == json_data["media_id"]):
                    error = False
                    break

            if(error == True):
                raise Exception("メディアがアップロードされていません。")

            #メディアテーブルを更新
            json_data = request.json
            media = Media(
                auther_user_id = userId,
                auther_ip = request.remote_addr,
                media_id = json_data["media_id"],
                content_type = json_data["content_type"],
            )
            g.db.session.add(media)
            g.db.session.commit()
            
            return make_response(f'''
{{
    "status": "OK"
}}
''')
        except Exception as e:
            return make_response(
                jsonify(
                        {
                            "state": "error"
                        },
                    )
                )

@app.route('/api/1.0/media/next_id', methods=['GET'])
def getNextMediaID():
    """
    ☆

    Returns:
        次に登録するメディアIDの値を取得する
    """
    if request.method == 'GET':
        try:
            #次のIDを取得・更新する
            info = g.db.session.query(Info).filter(Info.info_id==1).first()
            info.next_media_id += 1
            g.db.session.commit()
            
            #DBから次の番号を取得
            return make_response(f'''
{{
    "status": "OK",
    "next_media_id": {info.next_media_id},
    "next_media_id_str": "{info.next_media_id}"
}}
''')
        
        except Exception as e:
            pass
    
    return make_response(
        jsonify(
                {
                    "state": "error"
                },
            )
        )
         
         
#イベント関連--------------------------------------------------------

@app.route('/api/1.0/events/{event_id}', methods=['GET'])
def getEvents(event_id):
    """
    ☆TODO 未完成
    イベントの情報を取得する
    Args:
        event_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    userId = getUser()["user_id"]

    #
    event = g.db.session.query(Event).filter(Event.event_id == event_id).first()

    #
    j = {
        "data": {
            "images": [
                "http://ksadf.jpg",
                "http://fdsaf.jpg",
                ],
            "event_title": "○○展",
            "overview": "○○の個展です。",
            "latitude": "123",
            "longitude": "123",
        }
    }

    return "OK"

    return jsonify(j)       

def fetchEventMediaList(event_id):
    """
    DBからイベントのメディアを取得する

    返却地の例:
        [
            {
                "path": "gs://gallery-log-859ae.appspot.com/media/123"
            }
        ]
    """
    dbEventMediaList = g.db.session.query(EventMediaList)

    dbEventMediaList = dbEventMediaList.filter(
        and_(
            EventMediaList.event_id == event_id
        )
    )

    # #イベントテーブルとイベントメディアリストテーブルを外部結合する
    # dbEventMediaList = dbEventMediaList.join(
    #     EventMediaList,
    #     EventMediaList.event_id == Event.event_id,
    #     isouter = True)

    # #インデックスで並べ替える
    # dbEventMediaList = dbEventMediaList.order_by(EventMediaList.index)
    
    #データを取得する
    dbEventMediaList = dbEventMediaList.all()

    #オブジェクトデータを作成する
    eventMediaList = []
    for eventMedia in dbEventMediaList:
        eventMediaList.append(
            {
                "media_id_str": str(eventMedia.media_id)
            }
        )

    return eventMediaList

@app.route('/api/1.0/eventmeta/', methods=['GET'])
def getEventMeta():
    '''
    イベントにメタデータを追加する

    Query parameters:
        event_id(String): メタデータを追加するポストID

    JSON body parameters:
        meta_key(String): 取得するメタデータのキー
    '''
    try:
        #キーを取得する
        meta_key = None
        if 'meta_key' in request.args:
            meta_key = request.args["meta_key"]

        #値を取得する
        meta_value = None
        if 'meta_value' in request.args:
            meta_value = request.args["meta_value"]

        #イベントIDを取得する
        event_id = None
        if 'event_id' in request.args:
            event_id = request.args["event_id"]
        
        #メタデータを取得する
        metaList = _getEventMeta( event_id, meta_key, meta_value)

        #コミットする
        g.db.session.commit()


        return make_response(
            jsonify(
                {
                    'status': 'OK',
                    'data': metaList
                }
            )
        )
        

    except Exception as e:
        #ロールバック
        g.db.session.rollback()

        return make_response(
            jsonify(
                    {
                        "state": "error"
                    },
                )
            )
    
def _getEventMeta( event_id = None, meta_key = None, meta_value = None):
    dbMeta = g.db.session.query(EventMetaData)

    andArg = []
    if event_id != None:
        andArg.append(EventMetaData.event_id == int(event_id))

    if meta_key != None:
        andArg.append(EventMetaData.meta_key == meta_key)

    if meta_value != None:
        andArg.append(EventMetaData.meta_value == meta_value)
    
    dbMeta = dbMeta.filter(
                        and_(*andArg)
                    )

    dbMeta = dbMeta.all()

    return EventMetaDataSchema(many=True).dump(dbMeta)

@app.route('/api/1.0/eventmeta/', methods=['POST'])
def postEventMeta():
    '''
    イベントにメタデータを保存する
    '''
    try:
        event_id = request.json["event_id"] #値が存在するかを確認する
        meta_key = request.json["key"] #値が存在するかを確認する
        meta_value = request.json["value"] #値が存在するかを確認する
        type = None

        #typeを取得する
        try:
            type = request.json["type"] #値が存在するかを確認する
        except:
            pass

        #DBにメタデータを挿入する
        _postEventMeta( type, event_id, meta_key, meta_value)

        g.db.session.commit()

        return make_response(
                jsonify(
                    {
                        'status': 'OK',
                    }
                )
            )

    except Exception as e:
        #ロールバック
        g.db.session.rollback()

        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                )
            )


def _postEventMeta( type, event_id, meta_key, meta_value):
    '''
    '''
    #typeがsetだった場合、既存の値を削除する
    if type == "set":
        #古いイベントの画像のリストの情報を削除する
        g.db.session.query(EventMetaData).filter(EventMetaData.event_id == event_id).delete()

    meta = EventMetaData()
    meta.event_id = int(event_id)
    meta.meta_key = meta_key
    meta.meta_value = meta_value
    
    g.db.session.add(meta)


@app.route('/api/1.0/eventmeta/', methods=['DELETE'])
def deleteEventMeta():
    try:
        event_id = request.headers["event-id"] #値が存在するかを確認する

        _deleteEventMeta(event_id)

        g.db.session.commit()

        return make_response(
                jsonify(
                    {
                        'status': 'OK',
                    }
                )
            )

    except Exception as e:
        #ロールバック
        g.db.session.rollback()

        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                )
            )
    
def _deleteEventMeta(event_id):
    #古いイベントの画像のリストの情報を削除する
    g.db.session.query(EventMetaData).filter(EventMetaData.event_id == event_id).delete()


@app.route('/api/1.0/events/search/all', methods=['GET'])
def getEventsSearchAll():
    """
    ☆
    イベントの内容を検索しIDのリストを得る

    ■レスポンスメッセージの例
    {
        "data": [
            {
                "event_id_str": "1"
            },
            {
                "event_id_str": "2"
            }
        ]
    }
    """ 
    if request.method == 'GET':
        try:
            #ユーザーの情報を取得する
            fbUser = getUser()

            #
            dbEvents = g.db.session.query(Event)
            
            #タイトルと概要にキーワードが含まれるイベントに絞り込む
            try:
                q = request.args["q"] #値が存在するかを確認する
                dbEvents = dbEvents.filter(
                    or_(
                        Event.title.like(f'%{q}%'),
                        Event.overview.like(f'%{q}%'),
                        )
                    )
            except Exception as e:
                pass

            #イベントIDで絞り込む
            try:
                event_id = request.args["event_id"] #値が存在するかを確認する
                dbEvents = dbEvents.filter(
                    Event.event_id == event_id
                    )
            except Exception as e:
                pass
            
            #終了した展示は表示しない
            #（※開催日が未定の展示会も表示しません）
            try:
                request.args["exclude-ended"] #値が存在するかを確認する
                if request.args["exclude-ended"] == "true":
                    dbEvents = dbEvents.filter(
                        Event.end_date <= datetime.today()
                )
            except Exception as e:
                pass
            
            #開催中のみ表示
            try:
                request.args["open"] #値が存在するかを確認する
                if(request.args["open"] == "true"):
                    dbEvents = dbEvents.filter(
                        and_(
                            Event.start_date <= datetime.today(),
                            Event.end_date >= datetime.today(),
                            )
                        )
            except Exception as e:
                pass

            #評価で絞り込む
            try:
                request.args["rate"] #値が存在するかを確認する

                if(float(request.args["rate"]) > 0.0):
                    dbEvents = dbEvents.filter(
                            Event.rating >= float(request.args["rate"]),
                        )
            except Exception as e:
                pass
            
            
            # #開催日で絞り込む
            # try: 
            #     andArg = []

            #     #値が存在するかを確認する
            #     try:
            #         dt = datetime.datetime.strptime( request.args["since"], '%Y-%m-%d')
            #         andArg.append(Event.end_date < dt)
            #     except Exception as e:
            #         pass

            #     try:
            #         dt = datetime.datetime.strptime( request.args["until"], '%Y-%m-%d')
            #         andArg.append(dt < Event.start_date)
            #     except Exception as e:
            #         pass


            #     if len(andArg) > 0:
            #         dbEvents = dbEvents.filter(
            #             not_(
            #                 and_(*andArg)
            #             )
            #         )
            # except Exception as e:
            #     pass

            #開催日で絞り込む
            try: 
                andArg = []
                since = g.MinDate
                until = g.MaxDate

                #値が存在するかを確認する
                try:
                    since = datetime.datetime.strptime( request.args["since"], '%Y-%m-%d')
                except Exception as e:
                    pass

                try:
                    until = datetime.datetime.strptime( request.args["until"], '%Y-%m-%d')
                except Exception as e:
                    pass

                dbEvents = dbEvents.filter(
                    and_(
                        since <= Event.end_date,
                        until >= Event.start_date
                    ),
                )

                # dbEvents = dbEvents.filter(
                #     not_(
                #         and_(
                #             until < Event.start_date,
                #             Event.end_date < since,
                #         ),
                #     )
                # )

                # dbEvents = dbEvents.filter(
                #     or_(
                #         and_(
                #             Event.start_date <= since,
                #             until < Event.end_date,
                #         ),
                #         since <= Event.end_date,
                #         Event.start_date <= until
                #     )
                # )
            except Exception as e:
                pass
            
            #開催場所で絞り込む
            #TODO このコードは正常に動作するか自信が無いので、あとできちんとテストする事
            try:
                request.args["places"] #値が存在するかを確認する
                places = request.args["places"].split(',')
                orArg = []
                for place in places:
                    orArg.append(Event.prefecture == place)
                dbEvents = dbEvents.filter(
                                    or_(*orArg)
                                )
            except Exception as e:
                pass


            #投稿者IDで絞り込む
            try:
                request.args["poster-id"] #値が存在するかを確認する

                #絞り込む条件を作成する
                poster_id = request.args["poster-id"]

                dbEvents = dbEvents.filter(
                                    Event.auther_user_id == poster_id
                                )
            except Exception as e:
                pass


            #ブックマークで絞り込む
            try:
                request.args["bookmark-group-ids"] #値が存在するかを確認する

                #絞り込む条件を作成する
                bookmark_group_ids = request.args["bookmark-group-ids"].split(',')
                orArg = []
                for bookmark_group_id in bookmark_group_ids:
                    orArg.append(Bookmark.bookmark_group_id == int(bookmark_group_id))
                dbEvents = dbEvents.filter(
                                    or_(*orArg)
                                )
                
                # #イベントテーブルとブックマークテーブルを紐づける
                dbEvents = dbEvents.outerjoin(
                    Bookmark,
                    Event.event_id == Bookmark.target_id
                )
                
            except Exception as e:
                pass


            #ping_statusで絞込
            try:
                ping_status = request.args["ping-status"] #値が存在するかを確認する

                dbEvents = dbEvents.filter(Event.ping_status == ping_status)
            except Exception as e:
                pass

            #post_parentで絞込
            try:
                post_parent = request.args["post-parent"] #値が存在するかを確認する

                dbEvents = dbEvents.filter(Event.post_parent == post_parent)
            except Exception as e:
                pass

            #post_typeで絞込
            try:
                post_type = request.args["post-type"] #値が存在するかを確認する

                dbEvents = dbEvents.filter(Event.post_type == post_type)
            except Exception as e:
                pass


            #ソート
            try:
                request.args["sort"] #値が存在するかを確認する
                
                #投稿日が古い順
                if(request.args["sort"] == "post-date"):
                    dbEvents = dbEvents.order_by(Event.create_time)

                #投稿日が新しい順
                if(request.args["sort"] == "post-date-desc"):
                    dbEvents = dbEvents.order_by(desc(Event.create_time))

                #評価が高い順
                if(request.args["sort"] == "rating-desc"):
                    dbEvents = dbEvents.order_by(desc(Event.rating))

                #終了日が近い順
                if(request.args["sort"] == "nearest-end-date-asc"):
                    dbEvents = dbEvents.order_by(Event.end_date)

                #ブックマークが新しい順
                if(request.args["sort"] == "bookmark-date-desc"):
                    dbEvents = dbEvents.order_by(desc(Bookmark.create_time))
                
            except Exception as e:
                pass
            
            
            #limit
            try:
                count = request.args["count"] #値が存在するかを確認する

                dbEvents = dbEvents.limit(count)

            except Exception as e:
                pass

            #offset
            try:
                start = request.args["start"] #値が存在するかを確認する

                dbEvents = dbEvents.offset(start)

            except Exception as e:
                pass

            
            #イベントを取得する
            printSql(dbEvents)
            dbEvents = dbEvents.all()
            
            g.db.session.commit()
            
            events = EventSchema(
                            many=True,
                        ).dump(dbEvents)
            
            for event in events:
                event["media"] = fetchEventMediaList(event["event_id"])
            
            #メディアを追加する 

            return make_response(
                jsonify(
                    {
                        'status': 'OK',
                        'data':
                        {
                            "events": events
                        }
                   }
                )
            )

        except Exception as e:
            #ロールバック
            g.db.session.rollback()

            print("処理に失敗しました")

        g.db.session.rollback()
    
    return make_response(
            jsonify(
                {
                    "state": "error"
                },
                )
            )

route = '/api/1.0/events'
@app.route(route, methods=['POST'])
def PostEvent():
    """
    ☆TODO
    イベントを投稿する
    
    リクエストメッセージのbodyにはjsonを渡します
    各要素名はAPIのクラスの要素名と同じです。
    例
■headers
"Content-Type": "application/json"
"content-type": "application/json"
"Authorization": <トークン>
■body
{
    "title": "○○展",
    "overview": "○○の個展です。",
    "latitude": 0,
    "longitude": 0,
    "place": {
        "google_place_id": "DSLKTJ3131W3O31D31SLR",
        "name": "○○ギャラリー",
        "address": "○○県○○市○○丁目○○番地"
        "latitude": 0,
        "longitude": 0,
        "iso_3166_2": "13"
    },
    "start_date": "2025-1-1",
    "end_date": "2025-2-1",
    "media": [
        {
            "media_id": 0
        },
        {
            "media_id": 2
        }
    "metadata": [
        {
            "key": "aaa",
            "value": "111",
        },
        {
            "key": "bbb",
            "value": "222",
        },
        {
            "key": "bbb",
            "value": "333",
        }
    ]
  ]
}
    """

    try:
        userId = getUser()["user_id"]

        #リミットステータスを確認する
        res = consumeLimit( userId, inspect.currentframe().f_code.co_name, 60, 1)
        if res.state == CheckLimitResultState.ERROR:
            raise Exception("アクセス数が上限に達しました")

        # res = consumeLimit(
        #     user_id = userId,
        #     status_name = "POST " + route,
        #     limitMax = 100
        #     )
        
        # if res.state == CheckLimitResultState.ERROR:
        #     raise Exception("")
        

        #フォルダを取得する
        bucket = storage.bucket(config.FBStorage)
        
        #
        tempImagePaths = None

        #POSTメソッドだったら・・・
        if request.method == 'POST':
            #リクエストボディーで渡されたデータを保存する
            reqJson = request.json
            
            #TODO この処理は未完成です
            #フォームから画像が渡されていればそれを一時フォルダに保存する
            #※画像が渡されて居ない場合、クライアントが直接クラウドに一時画像をアップロードしているので、ここでは一時画像を保存しない。
            # if 'tempImagePaths' in request.form:
                
            #     tempImagePaths = []
                
            #     images = request.files.getlist()
            #     for image in images:
            #         #画像オブジェクトを取得
            #         file = image
                    
            #         #一時的なファイル名を作成
            #         uid = uuid.uuid1()  #ファイル名に使用するユニークな文字列を作成する
            #         root, ext = os.path.splitext(file.filename)     #拡張子を取得する
            #         tempPath = str(uid) + ext
                    
            #         #一時的なフェイル名をリストに保存する
            #         tempImagePaths.append(tempPath)

            #         #ファイルのアップロード
            #         blob = bucket.blob("cat.png")
            #         blob.upload_from_filename("./" + tempPath)
            
            #DBにEventを追加する-------------------------------

            event = None

            #イベントIDを取得する
            event_id = normalizeValue( reqJson, "event_id")

            #新規作成だった場合、イベントを作成する
            if event_id == None:
                #新たにイベントクラスを作成する
                event = Event()

                #クライアントから渡された値を代入する
                assignmentEvent(event, reqJson)

            #更新だった場合のイベントDBから取得する
            elif event_id != None:
                #DBからIDのイベントを取得する
                event = g.db.session.query(Event).filter(Event.event_id == event_id).first()


            #クライアントから渡された値を代入する
            if event != None:
                assignmentEvent(event, reqJson)
            else:
                raise Exception("イベントの作成に失敗しました。")
        
            #イベントをDBに追加する
            g.db.session.add(event)

            # プライマリーキーを生成する
            g.db.session.flush()  

            
            #メディアのリストをDBに挿入する---------------------------
            
            #予め正常に画像がアップロードされたか確認する
            for reqOneMediaJson in reqJson["media"]:

                #ファイルを取得する
                blob = bucket.blob("media/" + str(reqOneMediaJson["media_id"]))

                #ファイルが存在していなければ例外を発生させる
                if(blob.exists() == False):
                    raise Exception("ファイルが正常にアップロードされていません。")
                

            #古いイベントの画像のリストの情報を削除する
            g.db.session.query(EventMediaList).filter(EventMediaList.event_id == event_id).delete()

            #DBに画像の情報を追加する
            for i, reqOneMediaJson in enumerate(reqJson["media"]):

                #DB上に既に、同じIDの画像が存在するか確認する
                dbMedia = g.db.session.query(Media).filter(Media.media_id == reqOneMediaJson["media_id"]).first()

                #メディアがDBに存在していなければメディアの情報をDBに追加する
                if dbMedia == None:
                    media = Media(
                        media_id = reqOneMediaJson["media_id"],
                        auther_user_id = userId,    #get()はキーが存在しない場合Noneが返す
                        auther_ip = request.remote_addr,
                        #contents_type = jsonMedia["contents_type"]
                        )
                    g.db.session.add(media)
                
                #イベントのメディアテーブルを保存する
                eventMediaList = EventMediaList(
                    media_id = reqOneMediaJson["media_id"],
                    event_id = event.event_id,
                    index = i
                )
                g.db.session.add(eventMediaList)


            #履歴を新規作成しDBに追加する---------------------------
            newRevision = Event()

            #イベントに値を代入する
            assignmentEvent(newRevision, reqJson)
            newRevision.event_id = None
            newRevision.post_status = "inherit"
            newRevision.ping_status = "closed"
            newRevision.post_parent = event.event_id
            newRevision.post_type = "revision"

            g.db.session.add(newRevision)

            g.db.session.flush()


            #新規作成した履歴のメタデータを新規作成・保存する-------------------------
            if "metadata" in reqJson:
                for meta in reqJson["metadata"]:
                    _postEventMeta( "add", newRevision.event_id, meta["meta_key"], meta["meta_value"])
            

            #メディアの履歴を保存する---------------------------

            #DBに画像の情報を追加する
            for i, reqOneMediaJson in enumerate(reqJson["media"]):
                #イベントのメディアテーブルを保存する
                eventMediaList = EventMediaList(
                    media_id = reqOneMediaJson["media_id"],
                    event_id = newRevision.event_id,
                    index = i
                )
                g.db.session.add(eventMediaList)

            #コミットする
            g.db.session.commit()
        
    except Exception as e:
        #ロールバック
        g.db.session.rollback()

        return make_response(
            jsonify(
                {
                    "status": "Error",
                    "message": str(e)
                },
            )
        )

    return make_response(
    
        jsonify(
            {
                'status': 'OK',
                "message": "正常にイベントが投稿されました。"
            },
        )
    )



@app.route('/api/1.0/events/<event_id>', methods=['DELETE'])
def deleteEvent(event_id):
    try:
        event = g.db.session.query(Event).filter_by(event_id=str(event_id)).first()
        g.db.session.delete(event)

        g.db.session.commit()
        
        return make_response(
            jsonify(
                    {
                        "data": {
                            "deleted": True
                        }
                    },
                )
            )

    except Exception as e:
        pass

    return make_response(
        jsonify(
                {
                    "data": {
                        "deleted": False
                    }
                },
            )
        )

@app.route('/api/1.0/events/update_status', methods=['POST'])
def updateEventPostStatus():
    '''
    ポストステータスを更新する
    '''
    try:
        user = getUser()

        # #権限を確認する
        # roles = getUserRoles(dbUser.user_role_group_id)
        # user["role_group_name"] = roles["role_group_name"]
        # user["roles"] = roles["roles"]

        #Eventを取得・更新する
        dbEvent = g.db.session.query(Event).filter(Event.event_id == request.json["post_status"]).all()
        dbEvent.post_status = post_status
        g.db.session.commit()
        
        return make_response(
            jsonify(
                    {
                        "data": {
                            "deleted": True
                        }
                    },
                )
            )

    except Exception as e:
        pass

    return make_response(
        jsonify(
                {
                    "data": {
                        "deleted": False
                    }
                },
            )
        )


def dateToDatetime(d):
    """
    date型をdatetime型に変換する
    """
    
    #combine(): 日付の型と時刻の型を組み合わせる
    t = datetime.time( 0, 0, 0, 0)
    dt = datetime.datetime.combine(d, t)
    return pytz.timezone('Asia/Tokyo').localize(dt)


def fetchEventFromRDB(event_id):
    """
    DBからイベントを取得しオブジェクトデータを返す
    """
    try:
        #EventMediaListテーブルからデータを取得する---------------
        
        #DBから取得したメディアの情報を入れる変数
        media = []
        
        #DBからデータを取得する
        dbEventMediaList = g.db.session.query(EventMediaList) \
                            .filter(EventMediaList.event_id == str(event_id)) \
                            .order_by(asc(EventMediaList.index)) \
                            .all()
        for eventMedia in dbEventMediaList:
            media.append(
                {
                    "media_id_str": str(eventMedia.media_id)
                }
            )
        
        
        #Eventテーブルからデータを取得する-------------------------
        
        dbEvent = g.db.session.query(Event) \
                            .filter(Event.event_id == str(event_id)) \
                            .first()
                            
        #取得したデータを結合する---------------------------
        
        data = {
            "event_id_str": str(dbEvent.event_id),
            "auther_user_id_str": str(dbEvent.auther_user_id),
            "title": dbEvent.title,
            "overview": dbEvent.overview,
            "latitude": dbEvent.latitude,
            "longitude": dbEvent.longitude,
            "start_date": dateToDatetime(dbEvent.start_date),
            "end_date": dateToDatetime(dbEvent.end_date),
            "create_time": dbEvent.create_time,
            "media": media
        }
        
        return data
       
    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "state": "error"
                    },
                )
            )

@app.route('/api/1.0/events/<event_id>/make_pre_data', methods=['POST'])
def makeEventPreData(event_id):
    """
    """
    try:
        #データベースからイベントデータを読み込む
        data = fetchEventFromRDB(event_id)
        
        # #アプリケーションのデフォルト認証情報が自動的に作成されます。
        # app = firebase_admin.initialize_app()
        
        # Use a service account.
        #cred = credentials.Certificate('path/to/serviceAccount.json')

        #app = firebase_admin.initialize_app(cred)

        db = firestore.client()
        
        doc_ref = db.collection("events").document(str(event_id))
        doc_ref.set(
                data
            )
        
        return make_response(
            
            jsonify(
                {
                    "status": "OK",
                    "message": "イベントデータの作成に成功しました。"
                },
                
                
                )
            )


    except Exception as e:
        return make_response(
            jsonify(
                    {
                        "state": "error"
                    },
                )
            )
    

@app.route('/api/1.0/events/<event_id>/make_json', methods=['POST'])
def makeJson(event_id):
    """
    イベントページを作成する
    """
    try:
        data = fetchEventFromRDB(event_id)
        
        j = jsonify(data)

        #イベントを表すjsonをサーバーにアップロードする------------------
        bucket = storage.bucket("gallery-log-859ae.appspot.com")
        blob = bucket.blob("events/" + str(dbEvent.event_id) + ".json")
        blob.upload_from_string(
            data = j,
            content_type="application/json"
            )
       
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "state": "error"
                },
                
                
                )
            )
    
    return make_response(
        jsonify(
                {
                    "state": "ok",
                    "message": "イベントデータの作成に成功しました。"
                },
            )
        )


#通知関連(トピック)----------------------------------------------------

@app.route('/api/1.0/topic', methods=['POST'])
def postTopic():
    '''トピックを作成する
    '''
    try:
        topic = Topic()
        topic.topic_name = request.json["topic_name"]
        
        g.db.session.add(topic)

        g.db.session.commit()
    except Exception as e:
        return None
    

@app.route('/api/1.0/topic/all', methods=['GET'])
def getAllTopics():
    '''
    全てのトピックのリストを取得する
    '''
    try:
        topicList = g.db.session.query(Topic).all()
        topicList = TopicSchema(
            many=True,
        ).dump(topicList)

        return make_response(
            jsonify(
                {
                    "status": "ok",
                    "data": {
                        "topics": topicList
                    }
                }
            )
        )

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )


#通知関連（通知）----------------------------------------------------

@app.route('/api/1.0/notification', methods=['POST'])
def postNotification():
    '''
    通知を送るする
    '''
    try:
        notification = Notification()
        notification.send_target_type = request.json["send_target_type"]
        notification.send_target = request.json["send_target"]
        notification.title = request.json["title"]
        notification.body = request.json["body"]
        notification.link = request.json["link"]

        g.db.session.add(notification)

        g.db.session.commit()
        
        
        return make_response(
            jsonify(
                {
                    "status": "OK"
                }
            )
        )
    
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )
    

@app.route('/api/1.0/notification', methods=['GET'])
def getNotification():
    '''
    ユーザーに送られた通知をすべて取得する
    '''
    try:
        user_id = getUser()["user_id"]

        #ユーザーが購読しているすべてのトピックのIDを取得する
        subscriberList = g.db.session.query(Subscriber).filter(
            Subscriber.user_id == user_id
        )

        #購読しているトピックに送信された通知を取得する為の条件を作成する
        orList = []
        for subscriber in subscriberList:
            orList.append(
                and_(
                    Notification.send_target_type == "topic",
                    Notification.send_target == subscriber.topic_id
                )
            )

        #自分と同じユーザーIDに向けられた通知を受け取る
        orList.append(
            and_(
                Notification.send_target_type == "user_id",
                Notification.send_target == user_id
            )
        )
        
        notificationList = g.db.session.query(Notification).filter(or_(*orList))

        printSql(notificationList)

        notificationList = notificationList.all()
        
        notificationList = NotificationScheme(
                                    many=True,
                                ).dump(notificationList)

        g.db.session.commit()

        return make_response(
            jsonify(
                {
                    "status": "OK",
                    "data": {
                        "notifications": notificationList
                    }
                }
            )
        )
        
    except Exception as e:
        print(e)
        
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )

#通知関連----------------------------------------------------

@app.route('/api/1.0/notification/register_user_token', methods=['POST'])
def postNotification_RegisterUserTokens():
    '''
    ユーザーIDにトークンを紐づける
    '''
    try:
        
        user_id = getUser()["user_id"]
        
        # if "Authorization" in request.headers:
        #     token = request.headers["Authorization"]
        
        userTokens = DeviceToken()
        userTokens.user_id = user_id
        userTokens.token = request.json["fcmToken"]
        g.db.session.add(userTokens)
        g.db.session.commit()

        return make_response(
            jsonify(
                {
                    "status": "OK",
                }
            )
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )   


@app.route('/api/1.0/user_tokens', methods=['DELETE'])
def deleteUserToekns():
    '''
    通知先のトークンを削除する
    '''
    try:
        g.db.session.query(DeviceToken). \
        filter(
            DeviceToken.token == request.json["token"]
        ).delete()
        
        g.db.session.commit()

        return make_response(
            jsonify(
                {
                    "status": "OK",
                }
            )
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )
    
@app.route('/api/1.0/register_token_to_topic', methods=['POST'])
def postRegisterTokenToTopic():
    '''
    トピック（複数のユーザーをまとめたグループのようなもの）にユーザートークンを追加する
    '''
    try:

        # トピックにトークンを追加する
        response = messaging.subscribe_to_topic( request.json["fcmTokens"], request.json["topic"])
        if response.errors.length != 0:
            raise Exception("トークンをトピックに追加できませんでした。")

        return make_response(
            jsonify(
                {
                    "status": "OK",
                }
            )
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )
    
@app.route('/api/1.0/delete_token_from_topic', methods=['POST'])
def deleteRegisterTokenToTopic():
    '''
    トピック（複数のユーザーをまとめたグループのようなもの）からユーザートークンを削除する
    '''
    try:
        # トピックにトークンを追加する
        response = messaging.unsubscribe_from_topic( request.json["tokens"], request.json["topic"])
        print(response)

        return make_response(
            jsonify(
                {
                    "status": "OK",
                }
            )
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )
    
    
@app.route('/api/1.0/send_message', methods=['POST'])
def send_message():
    '''
    ユーザーかトピックに通知を送る
    '''
    try:
       
        #    # サービスアカウントキーの読み込み
        #     cred = credentials.Certificate("serviceAccountKey.json")

        #     # FirebaseAdminの初期化
        #     firebase_admin.initialize_app(cred)

        # メッセージの作成
        message = messaging.Message(
            notification = messaging.Notification(
                title = request.json["title"],
                body = request.json["body"],
            ),
            webpush = messaging.WebpushConfig(

            ),
            token = request.json["token"],
            topic = request.json["topic"],
        )

        # メッセージの送信
        response = messaging.send(message)
        print("response:", response)

        #履歴を保存する
        notif =  Notification()
        notif.title = request.json["title"],
        notif.body = request.json["body"],
        notif.send_to = request.json["token"],

        return make_response(
            jsonify(
                {
                    "status": "OK",
                }
            )
        )
    
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": "error",
                }
            )
        )


#アクセス解析関連--------------------------------------------------------

@app.route('/api/1.0/analytics', methods=['POST'])
def postAnalytics():

    j = request.json

    analysisData = AnalyticsData()
    analysisData.url = j["url"]
    analysisData.access_aource_url = j["access_aource_url"]
    analysisData.user_id = j["user_id"]
    analysisData.access_source_ip = j["access_source_ip"]

    g.db.session.add(analysisData)

    g.db.session.commit()

    return make_response(
            jsonify(
                    {
                        "status": "OK"
                    }
                )
            )


#場所関連--------------------------------------------------------

@app.route('/api/1.0/places/search/all', methods=['GET'])
def getPlacesSearchAll():
    """
    """
    try:
        dbPlaces = g.db.session.query(Place)

        #タイトルと概要にキーワードが含まれるイベントに絞り込む
        try:
            q = request.args["q"] #値が存在するかを確認する
            dbEvents = dbEvents.filter(
                    or_(
                        Place.name.like(f'%{q}%'),
                        Place.address.like(f'%{q}%'),
                        )
                    )
        except Exception as e:
            pass
        
    except Exception as e:
        pass

#インデント関連--------------------------------------------------------

indentCount = 0
def getIndent():
    res = ""
    for _ in range(indentCount):
        res += "\t"
        
    return res

def incrementIndent():
    indentCount += 1
    
def decrementIndent():
    indentCount += 1
    
def resetIndent():
    indentCount = 0
    
    
#デバッグ関連--------------------------------------------------------

@app.route('/api/1.0/debug-info/')
def debugInfo():
    print("------ debug info------------------")
    print("__file__ : " + __file__)
    print("os.environ['HOME'] : " + expanduser("~"))
    
    return render_template(
        'index.html'
    )

@app.route('/api/1.0/debug/test')
def debugTest():
    return make_response('''
{{
    "state": "OK",
    "message": "Test OK"
}}
''')

@app.route('/api/1.0/debug/test2/', methods=['POST'])
def debugTest2():

    consumeLimit( 1, "state_name", 15, 15)

    res = make_response(
        jsonify(
            {

            }
        )
    )
    res.headers.set('Content-Type', request.content_type) # ヘッダ設定


def skeleton_SQL(type, params):
    try:
        type = Event

        #カンマ区切りのカラム名のリストを作成する
        first = True
        strColmNames = ""
        for key in params.keys():
            if(first != True):
                strColmNames += ", "
            else:
                first = False

            strColmNames += key

        #カンマ区切りの値のリストを作成する
        first = True
        strValues = ""
        for key in params.keys():
            if(first != True):
                strValues += ", "
            else:
                first = False

            if(isinstance(params[key], str) == True):
                strValues += "'" + params[key] + "'"
            else:
                strValues += str(params[key])

        #ON DUPLICATE KEY UPDATE用のリストを作成する
        first = True
        updateParams = ""
        for key in params.keys():
            if(first != True):
                updateParams += ",\n"
            else:
                first = False

            if(isinstance(params[key], str) == True):
                updateParams += key + " = " + "'" + params[key] + "'"
            else:
                updateParams += key + " = " + str(params[key])

        #SQL文を作成する
        sql = f"""INSERT INTO {type.__tablename__}({strColmNames}) VALUES ({strValues})
ON DUPLICATE KEY UPDATE 
{updateParams};"""
        
        g.db.session.execute(text(sql))

        #挿入・更新した要素のIDを返す
        res = g.db.session.execute(text("SELECT LAST_INSERT_ID()"))
        return res["LAST_INSERT_ID()"]
        
    except Exception as e:
        raise e

@app.route('/api/1.0/debug/insert_test_data', methods=['POST'])
def postTestData():
    try:
        #テーブルを作成する
        with app.app_context():
            g.db.create_all()
        
        #infoテーブルに要素を追加する
        info = Info()
        g.db.session.add(info)
        g.db.session.commit()
        
        #Eventテーブルにテストデータを挿入する
        for i in range(20):
            event = Event(
                title="〇〇展 " + str(i),
                overview="〇〇展 " + str(i),
                #開催日
                start_date = datetime.datetime.now() - datetime.timedelta(days=10) + datetime.timedelta(days=i),
                end_date = datetime.datetime.now() - datetime.timedelta(days=5) + datetime.timedelta(days=i)
            )
            g.db.session.add(event)

        for i in range(20):
            media = Media(
                content_type="image/jpeg",
            )
            g.db.session.add(media)

        for i in range(20):
            eventMediaList = EventMediaList(
                event_id = i,
                media_id = 1,
                index = 1,
            )
            g.db.session.add(eventMediaList)

            eventMediaList = EventMediaList(
                event_id = i,
                media_id = 2,
                index = i,
            )
            g.db.session.add(eventMediaList)
            
        g.db.session.commit()

        return '''
{{
    "state": "OK",
}}
'''
    except Exception as e:
        print(e)
        pass

    
    return '''
{{
    "state": "Error",
    "message": "RDBの初期化に失敗しました。"
}}
'''
   
#その他--------------------------------------------------------
 
# def initDB():
#     #DBに接続する
#     conn = mysql.connector.connect(
#         host = config.db_host,
#         #port='3306',
#         user = config.db_user,
#         password = config.db_password,
#         database = config.db_name
#         )

#     #カーソルを取得する
#     cur = conn.cursor()
    
#     #DBを選択する
#     sql = "use " + config.db_name
#     cur.execute(sql)
    
#     return conn, cur

@app.route('/api/1.0/init', methods=['POST'])
def init_db():
    try:
        #TODO ここで権限を取得すること

        #FBからユーザーを全て削除する-----------------------

        #全てのユーザーを取得する
        userIdList = []
        page = auth.list_users()
        while page:
            for user in page.users:
                userIdList.append(user.uid)
            # Get next batch of users.
            page = page.get_next_page()

        #全てのユーザーを削除する
        result = auth.delete_users(userIdList)

        print('Successfully deleted {0} users'.format(result.success_count))
        print('Failed to delete {0} users'.format(result.failure_count))
        for err in result.errors:
            print('error #{0}, reason: {1}'.format(result.index, result.reason))

            
        #テーブル関連--------------------------------------

        #テーブルを作成する
        #TODO テーブルを全て削除する(なぜか削除できない)
        g.db.drop_all()

        #テーブルを作成する
        g.db.create_all()
        
        #infoテーブルに要素を追加する
        info = Info(
            next_media_id = 0
        )
        g.db.session.add(info)
        g.db.session.flush()  # プライマリーキーが生成される

        #ユーザー権限グループを作成----------------------------------
        
        #ユーザー権限グループに要素を追加する
        userRoleGroup = UserRoleGroup(
            role_group_name = "開発者"
        )
        g.db.session.add(userRoleGroup)
        g.db.session.flush()  # プライマリーキーが生成される
        
        #権限グループに権限を追加する
        for role in g.rolesDeveloper:
            userRole = UserRole(
                user_role_group_id = userRoleGroup.user_role_group_id,
                value = role
            )
            g.db.session.add(userRole)

        #ユーザーグループを作成
        userRoleGroup = UserRoleGroup(
            role_group_name = "管理者"
        )
        g.db.session.add(userRoleGroup)
        g.db.session.flush()  # プライマリーキーが生成される

        #権限グループに権限を追加する
        for role in g.rolesAdmin:
            userRole = UserRole(
                user_role_group_id = userRoleGroup.user_role_group_id,
                value = role
            )
            g.db.session.add(userRole)

        #ユーザーグループを作成
        userRoleGroup = UserRoleGroup(
            role_group_name = "投稿者"
        )
        g.db.session.add(userRoleGroup)
        g.db.session.flush()  # プライマリーキーが生成される

        #権限グループに権限を追加する
        for role in g.rolesAuther:
            userRole = UserRole(
                user_role_group_id = userRoleGroup.user_role_group_id,
                value = role
            )
            g.db.session.add(userRole)

        #ユーザーグループを作成
        userRoleGroup = UserRoleGroup(
            role_group_name = "寄稿者"
        )
        g.db.session.add(userRoleGroup)
        g.db.session.flush()  # プライマリーキーが生成される

        #権限グループに権限を追加する
        for role in g.rolesAuther:
            userRole = UserRole(
                user_role_group_id = userRoleGroup.user_role_group_id,
                value = role
            )
            g.db.session.add(userRole)
            

        #--------------------------------------------------------

        if g.isDebug():
            #テストユーザーを作成する--------------------------------

            #テストユーザーを作成する
            fUser = auth.create_user(
                email='developer@a',
                email_verified=True,
                password='password',
                display_name='Test Developer',
                photo_url='http://www.example.com/12345678/photo.png',
                disabled=False)
            
            #テスト用のユーザーを作成する
            user = User()
            user.user_id = fUser.uid
            user.name = "Test Developer"
            user.username = "test_developer"
            user.user_role_group_id = 1
            g.db.session.add(user)

            #テストユーザーを作成する
            fUser = auth.create_user(
                email='admin@a',
                email_verified=True,
                password='password',
                display_name='Test Admin',
                photo_url='http://www.example.com/12345678/photo.png',
                disabled=False)
            
            #テスト用のユーザーを作成する
            user = User()
            user.user_id = fUser.uid
            user.name = "Test Admin"
            user.username = "test_admin"
            user.user_role_group_id = 2
            g.db.session.add(user)

            #テストユーザーを作成する
            fUser = auth.create_user(
                email='auther@a',
                email_verified=True,
                password='password',
                display_name='Test Auther',
                photo_url='http://www.example.com/12345678/photo.png',
                disabled=False)
            
            #テスト用のユーザーを作成する
            user = User()
            user.user_id = fUser.uid
            user.name = "Test Auther"
            user.username = "test_auther"
            user.user_role_group_id = 3
            g.db.session.add(user)

            #テストユーザーを作成する
            fUser = auth.create_user(
                email='subscriber@a',
                email_verified=True,
                password='password',
                display_name='Test subscriber',
                photo_url='http://www.example.com/12345678/photo.png',
                disabled=False)
            
            #テスト用のユーザーを作成する
            user = User()
            user.user_id = fUser.uid
            user.name = "Test Subscriber"
            user.username = "test_subscriber"
            user.user_role_group_id = 4
            g.db.session.add(user)


        #--------------------------------------------------------

        g.db.session.commit()

        return make_response("データベースの作成に成功しました。")
        
    except Exception as e:

        print("-------------")
        print(e)
        print("データベースの作成に失敗しました。")

        resq = make_response("データベースの作成に失敗しました。")
        return resq
        
#外部のREST APIを呼び出す-------------------------------------
@app.route('/api/1.0/debug/call_rest_api', methods=['POST'])
def callRestAPI():
    try:
        method = request.json["method"]
    except Exception as e:
        method = ""
        pass

    try:
        url = request.json["url"]
    except Exception as e:
        url = ""
        pass

    try:
        params = request.json["params"]
    except Exception as e:
        params = {}

    if method == "GET":
        res = requests.get( url, params=params)
    elif method == "POST":
        res = requests.post( url, params=params)
    else:
        pass

    return make_response(
        res.text
        )


#Util--------------------------------------------------------

def getUser():
    """
        ユーザー情報を取得する
    """

    fbUser = None

    idToken = request.headers.get("Authorization", None)
    if idToken != None:
        fbUser = auth.verify_id_token(idToken)

    return fbUser



#メタデータ関連----------------------------------------------------------

@app.route("/metadata/add", methods=["POST"])
def postMetadata():
    '''
    メタデータに要素を追加する

    JSON body parameters:
        overwrite(String): "true"にすると上書き
        type(String): "EventMetaData", "UserMetaData"など
        target_id(String): イベントID, ユーザーIDなど
        meta_key(String): メタデータのキー
        meta_value(String): メタデータの値
    '''
    try:
        overwrite = False

        #上書き指定を取得する
        if "overwrite" in request.json:
            if request.json["overwrite"] == "true":
                overwrite = True

        #上書き指定されていた場合、既存のデータを削除する
        if overwrite == True:
            deleteMetadata(
                request.json["type"],
                request.json["target_id"],
                request.json["meta_key"]
            )

        #新規にメタデータを挿入する
        metadata = MetaData()
        metadata.type = request.json["type"]
        metadata.target_id = request.json["target_id"]
        metadata.meta_key = request.json["meta_key"]
        metadata.meta_value = request.json["meta_value"]

        g.db.session.add(metadata)

        g.db.session.commit()

        return make_response(
                jsonify(
                        {
                            "status": "OK",
                        },
                    )
                )

    except Exception as e:
        g.db.session.rollback()
        return make_response(
                jsonify(
                        {
                            "status": "error",
                        },
                    )
                )


@app.route("/metadata/delete", methods=["POST"])
def DeleteMetadata():
    '''
    メタデータを削除する
    '''
    try:
        deleteMetadata(
            request.json["type"],
            request.json["target_id"],
            request.json["meta_key"],
        )

        g.db.session.commit()

        return make_response(
                jsonify(
                        {
                            "status": "OK",
                        },
                    )
                )

    except Exception as e:
        return make_response(
                jsonify(
                        {
                            "status": "error",
                        },
                    )
                )

def deleteMetadata(type, target_id, metaa_key):
    try:
        g.db.session.query(MetaData).filter(
            and_(
                MetaData.type == type,
                MetaData.target_id == target_id,
                MetaData.meta_key == metaa_key,
            )
        ).delete()

    except Exception as e:
        raise e