from flask import Blueprint

main_module = Blueprint('main', __name__)

from . import views, errors
from portal.auth.models import Permission


@main_module.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
