# pip install marshmallow


from book_library_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, date, timedelta
from flask_sqlalchemy import BaseQuery
from werkzeug.datastructures import ImmutableDict
import re
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import BinaryExpression
from flask import request, url_for
from typing import Tuple
from werkzeug.security import generate_password_hash, check_password_hash
# pip install pyjwt
import jwt
from flask import current_app

# from book_library_app import Config

# COMPARISON_OPERATOR_RE = re.compile(r"(.*)\[(gte|gt|lte|lt|)\]")

# kurs 23.Model Author
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    books = db.relationship('Book', back_populates='author', cascade='all, delete-orphan')

    # metoda repr zwraca tekstową reprezentacje modelu
    def __repr__(self):
        return f"<{self.__class__.__name__}>:{self.first_name} {self.last_name}"

    # chodzi o to ze jezeli w postmenie dodamy w nagłówku Params fields = id,firstname to ta funcja obsługuje zeby schema była dynamiczna
    # czyli jak nie dodamy fields to wyswietlą sie wszystkie inf o autorze
    # a jak dodamy fields = id,first_name lub inne to wyswetli sie tylko id i first_nme autore
    # kurs 31
    # funcje przeniesione do utils kurs 42
    # @staticmethod
    # def get_schema_args(fields: str) -> dict:
    #     schema_args = {"many": True}
    #     if fields:
    #         schema_args["only"] = [field for field in fields.split(',') if field in Author.__table__.columns]
    #     return schema_args

    # funcje przeniesione do utils kurs 42
    # @staticmethod
    # def apply_order(query:BaseQuery, sort_keys:str)->BaseQuery:
    #     if sort_keys:
    #         for key in sort_keys.split(","):
    #             desc = False
    #             if key.startswith("-"):
    #                 key = key[1:]
    #                 desc = True
    #             column_attr = getattr(Author, key, None)
    #             if column_attr is not None:
    #                 query = query.order_by(column_attr.desc()) if desc else query.order_by(column_attr)
    #     return query

    # funcje przeniesione do utils kurs 42
    # @staticmethod
    # def get_filter_argument(column_name: InstrumentedAttribute, value: str, operator:str) -> BinaryExpression:
    #     operator_mapping = {
    #         "==" : column_name == value,
    #         "gte": column_name >= value,
    #         'gt': column_name > value,
    #         "lte": column_name <= value,
    #         "lt": column_name < value,
    #     }
    #     return operator_mapping[operator]
    #
    # @staticmethod
    # # def apply_filter(query:BaseQuery, params: ImmutableDict)->BaseQuery:
    # def apply_filter(query:BaseQuery)->BaseQuery:
    #     # for param, value in params.items():
    #     for param, value in request.args.items():
    #         if param not in ('fields', 'sort','page', 'limit'):
    #             operator = "=="
    #             match = COMPARISON_OPERATOR_RE.match(param)
    #             if match is not None:
    #                 param, operator = match.groups()
    #             column_attr = getattr(Author, param, None)
    #             if column_attr is not None:
    #                 if param == "birth_date":
    #                     try:
    #                         value= datetime.strptime(value, '%d-%m-%Y').date()
    #                     except ValueError:
    #                         continue
    #                 filter_argument = Author.get_filter_argument(column_attr, value, operator)
    #                 query = query.filter(filter_argument)
    #     return query

    # funcje przeniesione do utils kurs 42
    # @staticmethod
    # def get_pagination(query:BaseQuery) -> Tuple[list, dict]:
    #     page = request.args.get('page', 1, type=int)
    #     limit = request.args.get('limit', Config.PER_PAGE, type=int)
    #     params = {key: value for key, value in request.args.items() if key != "page"}
    #     paginate_obj = query.paginate(page=page, max_per_page=limit, error_out=False)
    #     pagination = {
    #         "total_pages": paginate_obj.pages,
    #         "total_records": paginate_obj.total,
    #         # po dodaniu Bluprint przed "get_authors" dodajemuy authors
    #         "current_page": url_for("authors.get_authors", page=page, **params)
    #     }
    #     if paginate_obj.has_next:
    #         pagination["next_page"]= url_for("authors.get_authors", page=page+1, **params)
    #
    #     if paginate_obj.has_prev:
    #         pagination["previous_page"]= url_for("authors.get_authors", page=page-1, **params)
    #
    #     return paginate_obj.items,  pagination

    @staticmethod
    def additional_validation(param:str, value:str) -> date:
            if param == "birth_date":
                try:
                    value = datetime.strptime(value, '%d-%m-%Y').date()
                except ValueError:
                    value =None
            return value


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f'{self.title} - {self.author.first_name} {self.author.last_name}'

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_hashed_password(password: str) -> str:
        return generate_password_hash(password)


    def is_password_valid(self, password: str)-> bool:
        return check_password_hash(self.password, password)


    def generate_jwt(self):
        pyload = {
            "user_id": self.id,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(pyload, current_app.config.get('SECRET_KEY'))

class AuthorsSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(max=50))
    last_name = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date('%d-%m-%Y', required=True)
    books = fields.List(fields.Nested(lambda: BookSchema(exclude=['author'])))

    # funkcja odpowiedzialna sprawdzenie czy data nie jest wieksza od obecnej
    @validates("birth_date")
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f"Birth_date must be lover then {datetime.now().date()}")


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=50))
    isbn = fields.Integer(required=True)
    number_of_pages = fields.Integer(required=True)
    description = fields.String()
    author_id = fields.Integer(load_only=True)
    author = fields.Nested(lambda: AuthorsSchema(only=['id','first_name','last_name']))

    @validates('isbn')
    def validate_isbn(self, value):
        if len(str(value)) != 13:
            raise ValidationError('ISBN must contain 13 digits')
        # if value != Book.isbn:
        #     raise ValidationError('ISBN')


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    creation_date = fields.DateTime(dump_only=True)


class UserPasswordUpdate(Schema):
    current_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6, max=255))


authors_schema = AuthorsSchema()
book_schema = BookSchema()
user_schema = UserSchema()
user_password_update_schema = UserPasswordUpdate()