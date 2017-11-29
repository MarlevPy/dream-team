class Config(object):
    """
    Common configurations
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
