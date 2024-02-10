class Config:
    ENGINE = 'django.db.backends.postgresql'

class DevelopmentConfig(Config):
    NAME = ''
    USER = ''
    PASSWORD = ''
    HOST = ''
    PORT = ''
    EMAIL_HOST_USER=''
    EMAIL_HOST_PASSWORD=''  


class ProductionConfig(Config):
    NAME = ''
    USER = ''
    PASSWORD = ''
    HOST = ''
    PORT = ''
    EMAIL_HOST_USER=''
    EMAIL_HOST_PASSWORD=''


class TestingConfig(Config):
    NAME = ''
    USER = ''
    PASSWORD = ''
    HOST = ''
    PORT = ''
    EMAIL_HOST_USER=''
    EMAIL_HOST_PASSWORD=''
