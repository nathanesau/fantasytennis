import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PASS = os.environ['REDIS_PASS']
    REDIS_PORT = 6379
