import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATA_SOURCE = os.path.join(basedir, 'datasets')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
