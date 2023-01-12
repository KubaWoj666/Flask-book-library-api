# pip install python-dotenv
# pakiet ten wczytuje ustawienia z pliku a następnie ustawia je jako zmienne środowiskowe

from dotenv import load_dotenv
from pathlib import Path
import os

# tworzymy zmienną która będie przechwywała scieżkę do folderu Flask_api
# kurs 18 Pliki konfiguracujne
base_dir = Path(__file__).resolve().parent
# zmienna która przechowywije ścieżkę do pliku .env
# tak sie buduje ścieżki z pomocą klasy Path
env_file = base_dir / '.env'
# funkcja ktura załaduje załaduje ustawienia z pliku .env
# beda przechowywane w zmiennej środowiskowej
load_dotenv(env_file)

# dzieki modułowi os
class Config:
    # pu ustawieniu .flaekenv to juz jest nie potrzebne kurs 24.
    # DEBUG = True
    # dzieki temu os.environ.get wyciągamy zmienną środowiskową 'SECRET_KEY'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # po wprowadzeniu klasy deweloperskiej i testowej zostawiamy pusty srting co oznacza że ten argument będzie nadpisany przez klasy pochodne
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
    JWT_EXPIRED_MINUTES = 30


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')



class TestingConfig(Config):
    DB_FILE_PATH = base_dir / 'tests' / 'tests.db'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_FILE_PATH}"
    DEBUG = True
    TESTING = True

# to jest potrzebne przy wdażaniu do AWS
class ProductionConfig(Config):
    DB_HOST = os.environ.get('DB_HOST')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production' : ProductionConfig
}


