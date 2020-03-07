from flask import render_template, request, current_app
from flask_login import current_user

from . import main_module
from .. import User
from ..auth.models import Permission
from ..diagram.models import Diagram


@main_module.route('/', methods=['GET', 'POST'])
def index():

    if current_user.can(Permission.READ):
        diagrams = Diagram.query.filter_by(author_id=current_user.id).all()
    else:
        diagrams = []
    return render_template('index.html', diagrams=diagrams)


@main_module.route('/help', methods=['GET', 'POST'])
def help():

    return render_template('help.html')

@main_module.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')

@main_module.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.diagrams.order_by(Diagram.update_time.desc()).paginate(
        page, per_page=current_app.config['PAGE_SIZE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)