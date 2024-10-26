from flask import Blueprint
import g
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, asc, desc, not_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert  # on_conflict_do_update が使える
from sqlalchemy import func
from sqlalchemy.dialects import mysql
from flask import request
from flask import Flask, jsonify
from flask import make_response
from main import MetaData


#モジュールを登録
meta_data_module = Blueprint( "meta_data", __name__)


