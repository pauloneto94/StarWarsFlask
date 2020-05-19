import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'jose')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False