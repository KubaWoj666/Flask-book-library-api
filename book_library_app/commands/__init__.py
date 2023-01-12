from flask import Blueprint

db_manage_bp = Blueprint('db_manage_commends', __name__, cli_group=None)

from book_library_app.commands import db_manage_commends