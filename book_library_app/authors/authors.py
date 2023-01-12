# pip install webargs
# from book_library_app import app, db
from book_library_app import db
from flask import jsonify, request
from book_library_app.models import Author, AuthorsSchema, authors_schema
from webargs.flaskparser import use_args
from book_library_app.utils import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination, token_required
from book_library_app.authors import authors_bp

# po wprowadzeniu Blueprint zmieniamy dekorator @app na authors_bp
# @app.route('/api/v1/authors', methods=['GET'])
# po wprowadzeniu prefixu w __init__.py zmieniamy scieżkę
# @authors_bp.route('/api/v1/authors', methods=['GET'])
@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    # query które wyciąga wszystkich autorów
    # authors = Author.query.all()
    query = Author.query
    # many=True pozwala na przekazanie wielu obiektów
    # authors_schema = AuthorsSchema(many=True)
    # schema_args = Author.get_schema_args(request.args.get("fields"))
    # kurs42
    schema_args = get_schema_args(Author)
    # kurs42
    # query = Author.apply_order(query, request.args.get('sort'))
    query = apply_order(Author, query)
    # query = Author.apply_filter(query, request.args)
    # kurs 42
    # query = Author.apply_filter(query)
    query = apply_filter(Author, query)
    # kurs 42
    # items, pagination = Author.get_pagination(query)
    items, pagination = get_pagination(query, 'authors.get_authors')
    # authors = query.all()
    # authors_schema = AuthorsSchema(**schema_args)
    authors = AuthorsSchema(**schema_args).dump(items)
    return jsonify(
        {
            "success": True,
            # dump przekształca obiekty na format json i przekazujemy wyciagnięte obiekty z bazy danych
            # "data": authors_schema.dump(authors),
            "data": authors,
            "numbers of records": len(authors),
            "pagination": pagination
        })


@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    # metoda get_or_404 znajdzie rekord o podanym id tutaj author_id a jak podanego id nie bedzie zwóci błąd 404
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")

    return jsonify(
        {
            "success": True,
            'data': authors_schema.dump(author)
        }
    )


@authors_bp.route('/authors', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(authors_schema, error_status_code=400)
def create_author(user_id: int ,args: dict):
    author = Author(**args)
    db.session.add(author)
    db.session.commit()
    # data  bedzie  przechchowywać dane z ciela zapytania http
    # po zaintalowaniu modułu web args to nie potrzebne
    # kurs 27!! dróga połowa mniej wiecej
    # data = request.get_json()
    # first_name = data.get("first_name")
    # last_name = data.get("last_name")
    # birth_date = data.get("birth_date")
    # author = Author(first_name=first_name, last_name=last_name, birth_date=birth_date)
    # db.session.add(author)
    # db.session.commit()

    return jsonify(
        {
            "success": True,
            'data': authors_schema.dump(author)
        }
    ), 201

# kolejnosć dekoratorów ma znaczenie
@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(authors_schema, error_status_code=400)
# kolejnosć argumentów w funcji ma znaczenie
def update_author(user_id: int, args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")

    author.first_name = args["first_name"]
    author.last_name = args["last_name"]
    author.birth_date = args["birth_date"]

    db.session.commit()


    return jsonify(
        {
            "success": True,
            'data': authors_schema.dump(author)
        }
    )


@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
@token_required
def delete_author(user_id: int, author_id: int):
    author = Author.query.get_or_404(author_id, description=f"Author with id {author_id} not found")

    db.session.delete(author)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            'data': f"author with id {author_id} hase been deleted"
        }
    )










