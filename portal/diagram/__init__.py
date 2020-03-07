from flask import Blueprint

diagram_module = Blueprint('diagram', __name__)

from . import views, errors