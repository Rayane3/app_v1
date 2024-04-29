import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nzebbn°0"z1_jfz/caz'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///default.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


