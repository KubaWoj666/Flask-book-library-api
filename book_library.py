# from book_library_app import app
from book_library_app import create_app

app = create_app()

# po wprowadzeniu zmiennej środowiskowej w pliku flask.env ten if jet nie potrzebny
# kurs 24 migracja baz danych
# if __name__ == "__main__":
#     app.run(port=8000)