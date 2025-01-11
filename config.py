import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQL_ALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS')
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    PERMANENT_SESSION_LIFETIME = timedelta(int(os.environ.get('PERMANENT_SESSION_LIFETIME')))
    SESSOIN_PERMANENT = os.environ.get('SESSION_PERMANENT')