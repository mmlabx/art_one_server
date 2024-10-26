import socket
import sys
import os
import datetime
import config


#デバッグ関連--------------------------------------------------
def isDebug():
    #環境変数にデバッグモードが設定されていれば
    if os.getenv('MMLAB_DEBUG') != "true":
        return False

    return True

def isRelease():
    #デバッグモードだった場合Falseを返す
    if isDebug() == True:
        return False
    
    #モードフラグで二重にチェックする
    if config.mode != "release":
        return False
    
    return True

def setDebugSettings():
    #環境変数を設定する
    if isDebug() == True:
        #エミュレーター用のホストを環境変数に設定する
        os.environ["FIRESTORE_EMULATOR_HOST"]="localhost:8080"
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"]="localhost:9099"
        os.environ["FIREBASE_STORAGE_EMULATOR_HOST"]="localhost:9199"

        #FirebaseのプロジェクトIDを設定する
        os.environ["GCLOUD_PROJECT"]="gallery-log-859ae"


#リリースモード用の設定をする
def setReleaseSettings():
    if isRelease() == False:
        return

    #RDBの設定
    config.db_host = "34.168.179.64"
    config.db_name = "gallery-log-859ae:us-west1:art-one-rdb"
    config.db_user = "mega"
    config.db_password = "uK0yB^#LcKkzDgf=  "

    #Firebaseの設定
    config.FBStorage = "gallery-log-859ae.appspot.com"

    #接続するCloud SQLインスタンスを指定
    config.db_instance_connection_name = "gallery-log-859ae:us-west1:art-one-rdb"


#日付関連--------------------------------------------------
MinDate = datetime.date( 1000 , 1, 1)
MaxDate = datetime.date( 9999 , 12, 31)


#DB関連--------------------------------------------------
db = None
ma = None


#ユーザー権限--------------------------------------------------

#デベロッパーの権限
rolesDeveloper = [
    #Wordpressと同じ権限
    "activate_plugins",
    "create_users",
    "delete_others_pages",
    "delete_others_posts",
    "delete_pages",
    "delete_plugins",
    "delete_posts",
    "delete_private_pages",
    "delete_private_posts",
    "delete_published_pages",
    "delete_published_posts",
    "delete_themes",
    "delete_users",
    "edit_dashboard",
    "edit_others_pages",
    "edit_others_posts",
    "edit_pages",
    "edit_plugins",
    "edit_posts",
    "edit_private_pages",
    "edit_private_posts",
    "edit_published_pages",
    "edit_published_posts",
    "edit_theme_options",
    "edit_themes",
    "edit_users",
    "export",
    "import",
    "install_languages",
    "install_plugins",
    "install_themes",
    "list_users",
    "manage_categories",
    "manage_links",
    "manage_options",
    "moderate_comments",
    "promote_users",
    "publish_pages",
    "publish_posts",
    "read",
    "read_private_pages",
    "read_private_posts",
    "remove_users",
    "resume_plugins",
    "resume_themes",
    "switch_themes",
    "unfiltered_html",
    "unfiltered_upload",
    "update_core",
    "update_plugins",
    "update_themes",
    "upload_files",
    "ure_create_capabilities",
    "ure_create_roles",
    "ure_delete_capabilities",
    "ure_delete_roles",
    "ure_edit_roles",
    "ure_manage_options",
    "ure_reset_roles",
    "view_site_health_checks",
    #MMLab独自の権限
    "mmlab_show_developers_elements",   #デバッグ情報を表示する
    "mmlab_delete_event_organiser",      #イベントの主催者を削除する
]

#管理者の権限
rolesAdmin = [
    #Wordpressと同じ権限
    "activate_plugins",
    "create_users",
    "delete_others_pages",
    "delete_others_posts",
    "delete_pages",
    "delete_plugins",
    "delete_posts",
    "delete_private_pages",
    "delete_private_posts",
    "delete_published_pages",
    "delete_published_posts",
    "delete_themes",
    "delete_users",
    "edit_dashboard",
    "edit_others_pages",
    "edit_others_posts",
    "edit_pages",
    "edit_plugins",
    "edit_posts",
    "edit_private_pages",
    "edit_private_posts",
    "edit_published_pages",
    "edit_published_posts",
    "edit_theme_options",
    "edit_themes",
    "edit_users",
    "export",
    "import",
    "install_languages",
    "install_plugins",
    "install_themes",
    "list_users",
    "manage_categories",
    "manage_links",
    "manage_options",
    "moderate_comments",
    "promote_users",
    "publish_pages",
    "publish_posts",
    "read",
    "read_private_pages",
    "read_private_posts",
    "remove_users",
    "resume_plugins",
    "resume_themes",
    "switch_themes",
    "unfiltered_html",
    "unfiltered_upload",
    "update_core",
    "update_plugins",
    "update_themes",
    "upload_files",
    "ure_create_capabilities",
    "ure_create_roles",
    "ure_delete_capabilities",
    "ure_delete_roles",
    "ure_edit_roles",
    "ure_manage_options",
    "ure_reset_roles",
    "view_site_health_checks"
    #MMLab独自の権限
    "mmlab_delete_event_organiser",      #イベントの主催者を削除する
]

#投稿者の権限
rolesAuther = [
    #Wordpressと同じ権限
    "delete_posts",
    "delete_published_posts",
    "edit_posts",
    "edit_published_posts", 
    "publish_posts",
    "read",
    "upload_files",
]

#寄稿者の権限
rolesContributor = [
    #Wordpressと同じ権限
    "delete_posts",
    "edit_posts",
    "read",
]