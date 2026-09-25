class GeneralConfig(object):
    APP_NAME = 'LargeScale'
    SECRET_KEY = 'notsecured'

class DevelopmentConfig(GeneralConfig):
    SECRET_KEY = 'f3caaba548eb693cb6bdb16fdf010579abaf689f7fb6d478c246d685c2aee44f0f453a26'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/staycare_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False