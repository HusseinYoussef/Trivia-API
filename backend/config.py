import os
from flask_sqlalchemy import SQLAlchemy
from models import db


class DATABASE_URI:

    DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '2681997')

    def get_DB_url(self, env='dev'):

        self.DB_NAME = os.getenv(
                                'DB_NAME', 'trivia'
                                if env == 'dev' else 'trivia_test'
                            )
        DB_PATH = "postgresql://{}:{}@{}/{}".format(
                                                self.DB_USER,
                                                self.DB_PASSWORD,
                                                self.DB_HOST,
                                                self.DB_NAME
                                            )
        return DB_PATH

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, env='dev'):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI().get_DB_url(env)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
