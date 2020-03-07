from flask import Blueprint


auth_module = Blueprint('auth', __name__)
from . import views