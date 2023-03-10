# Book Library REST API
REST API for online library. It supports authors of books and books resources including authentication (JWT Token).

The documentation can be found in documentation.html or here

## Setup
- Clone repository
- Create database and user
- Rename .env.example to .env and set your values
# SQLALCHEMY_DATABASE_URI MySQL template
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<db_password>@<db_host>/<db_name>?charset=utf8mb4
- Create a virtual environment
python -m venv venv
Install packages from requirements.txt
pip install -r requirements.txt
Migrate database
flask db upgrade
Run command
flask run
NOTE

Import / delete example data from book_library_app/samples:

# import
flask db-manage add-data

# remove
flask db-manage remove-data
Tests
In order to execute tests located in tests/ run the command:

python -m pytest tests/

# Technologies / Tools
- Python 3.8.0
- Flask 1.1.2
- Alembic 1.4.2
- SQLAlchemy 1.3.16
- Pytest 5.4.3
- MySQL
- AWS
- Postman