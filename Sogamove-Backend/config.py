import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/sogamove'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

