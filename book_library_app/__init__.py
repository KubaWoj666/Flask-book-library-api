from flask import Flask
# po stworzeniu słownika config w pliku confit.py zmieniamy import kurs 62
# from config import Config
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# pip install -U Flask-SQLAlchemy
# pip install pymysql
# pip install cryptography
# pip install flask_migrate (instaluje alembic do migracji baz danych)


# Pózniej przenosimy to do funcji kurs 38
# app = Flask(__name__)
# # metoda from_object wczytuje ustawienia dla aplikacji z danego obiektu w tym przypadku z klasy Config
# app.config.from_object(Config)
# app_ctx = app.app_context()
# app_ctx.push()

# w ten sposub wiążeny instancje klasy flask z obiektem app
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# pos tworzeniu funkcjji create_app kues 38
db = SQLAlchemy()
migrate = Migrate()

# kod testujący czy poączenie do bazy danych sie powiodło
# query = "show databases"
# results = db.session.execute(query)
#
# for row in results:
#     print(row)

# po zmianie importu kurs 62
# def create_app(config_class=Config):
def create_app(config_name='development'):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    app.config.from_object(config[config_name])
    app_ctx = app.app_context()
    app_ctx.push()

    db.init_app(app)
    migrate.init_app(app, db)

    from book_library_app.commands import db_manage_bp
    from book_library_app.errors import errors_bp
    from book_library_app.authors import authors_bp
    from book_library_app.books import books_bp
    from book_library_app.auth import auth_bp
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(authors_bp, url_prefix='/api/v1')
    app.register_blueprint(books_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app


# po wprowadzeniu funkscji create_app() importy są niepotrzebne
# from book_library_app import authors
# from book_library_app import models
# from book_library_app.commands import db_manage_commends
# from book_library_app import errors


# @app.route('/')
# def index():
#     return "Hello world"