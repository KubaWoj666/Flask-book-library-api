# from book_library_app import app, db
from book_library_app import db
import json
from pathlib import Path
from book_library_app.models import Author, Book
from datetime import datetime
from book_library_app.commands import db_manage_bp

# to jest takie sprytne że dodaje nam komendy które możemy wpisać do konsoli
# komenda wygląda tak flask db-manage add-data flask db-manage remove-data

# Kurs 41
def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / "samples" / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


# po wprowadzeniu Blueprint zmieniamy dekorator @app na @db_manage_bp
@db_manage_bp.cli.group()
def db_manage():
    """database management comments"""
pass

@db_manage.command()
def add_data():
    """Ad sample data to database"""
    try:
        # po Blubrint trzeba dodać jeszcze jedno parent zeby odnieść sie poziom wyżej
        # authors_path = Path(__file__).parent.parent / "samples" / "authors.json"
        # with open(authors_path) as file:
        #     data_json = json.load(file)
        data_json = load_json_data("authors.json")
        for item in data_json:
                # zamiana daty z formatu string na obiekt tadetime a następnie na obiekt date
                # '%d-%m-%Y' to jest format zapisu taty (dzień-mieśąc-rok)
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)
        data_json = load_json_data("books.json")
        for item in data_json:
            book = Book(**item)
            db.session.add(book)

        db.session.commit()
        print("Data hes been successfully added to database")
    except Exception as exe:
        print("Unexpected error: {}".format(exe))




@db_manage.command()
def remove_data():
    """Remove all data from database"""
    try:
        # TRUNCATE usuwa dane i resetuje klucz podstawowy
        # db.session.execute('TRUNCATE TABLE authors')
        db.session.execute('DELETE FROM books')
        db.session.execute('ALTER TABLE books AUTO_INCREMENT = 1')
        db.session.execute('DELETE FROM authors')
        db.session.execute('ALTER TABLE authors AUTO_INCREMENT =1')
        db.session.commit()
        print("Data hes been successfully deleted")
    except Exception as exe:
        print("Unexpected error: {}".format(exe))

