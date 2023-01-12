 # plik potrzebny do aws
 # AWS automatycznie wyszukuje pliku applcation i z niego uruchamia aplikacje

from book_library_app import create_app


application = create_app('production')