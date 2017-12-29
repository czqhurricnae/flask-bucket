class BasicConfig:
    SECRET_KEY = "key"
    PAGELIMIT = 5
    UPLOAD_FOLDER = "static/Uploads"


class DevelopmentConfig(BasicConfig):
    DEBUG = True


class ProductionConfig(BasicConfig):
    DEBUG = True
    MYSQL_DATABASE_HOST = "localhost"
    MYSQL_DATABASE_DB = "BucketList"
    MYSQL_DATABASE_USER = "root"
    MYSQL_DATABASE_PASSWORD = "c"


class TestingConfig(BasicConfig):
    TESTING = True


config = {
    "develop": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
