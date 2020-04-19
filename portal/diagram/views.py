from flask import render_template, redirect, url_for, flash, request, current_app
from portal.diagram.models import Diagram, Tag
from portal.diagram import diagram_module
from portal.diagram.forms import ScriptForm, UploadForm
from portal.diagram.painter import Painter
from portal import logger
from portal import db
import os
import uuid
from flask_login import login_required, current_user

dir_path = os.path.dirname(os.path.realpath(__file__))

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'dot', 'dsl', 'json'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
@diagram_module.route('/upload', methods=['POST'])
def upload_diagram():
    form = UploadForm()
    input_content = ""
    if form.validate_on_submit():
        file = form.script_file.data
        logger.info('filename={}'.format(file.filename))
        if file and allowed_file(file.filename):

            file_content = file.read()
            if file_content:
                input_content = file_content.decode('UTF-8').strip()
            file.close()

            logger.info('File successfully uploaded: {}'.format(input_content))
    else:
        logger.info(form.errors)
    upload_form = UploadForm()
    script_form = ScriptForm()
    script_form.script_content.data = input_content
    return render_template('diagram.html', form=script_form, upload_form=upload_form)


@login_required
@diagram_module.route('/diagrams/search/<tag>', methods=['GET'])
def search_diagram(tag):
    diagrams = Diagram.query.all()
    return render_template('diagrams.html', diagrams=diagrams)

@login_required
@diagram_module.route('/diagrams', methods=['GET'])
def list_diagram():
    page = request.args.get('page', 1, type=int)
    pagination = Diagram.query.order_by(Diagram.update_time.desc()).paginate(
        page, per_page=current_app.config['PAGE_SIZE'],
        error_out=False)
    diagrams = pagination.items
    return render_template('diagrams.html', comments=diagrams,
                           pagination=pagination, page=page)

@login_required
@diagram_module.route('/diagrams/<int:id>', methods=['GET'])
def edit_diagram(id):
    upload_form = UploadForm()
    script_form = ScriptForm()
    diagram = Diagram.query.filter_by(diagram_id=id).first()
    if diagram:
        script_form.script_content.data = diagram.diagram_script
        script_form.diagram_name.data = diagram.diagram_name
        script_form.diagram_type.data = diagram.diagram_type
        script_form.diagram_id.data = diagram.diagram_id
        aTag = Tag.query.filter_by(id=diagram.tag_id).first()
        if aTag:
            script_form.diagram_tag.data = aTag.name

    return render_template('diagram.html', form=script_form, upload_form=upload_form, diagrams=[diagram])

@login_required
@diagram_module.route('/diagrams/<int:id>', methods=['DELETE'])
def delete_diagram(id):
    diagram = Diagram.query.get_or_404(id)
    db.session.delete(diagram)
    db.session.commit()
    return redirect(url_for('.list_diagram',
                            page=request.args.get('page', 1, type=int)))

@login_required
@diagram_module.route('/paint', methods=['GET', 'POST'])
def paint():
    upload_form = UploadForm()
    script_form = ScriptForm()
    if script_form.validate_on_submit():
        logger.info("submit: {} or save {}".format(script_form.submit_button.data, script_form.save_button.data))
        script_content = script_form.script_content.data
        image_path = "{}/../static".format(dir_path)
        image_name = "uml_{}.txt".format(uuid.uuid4())

        if script_form.diagram_name.data:
            image_name = script_form.diagram_name.data

        painter = Painter(image_name)
        painter.path = image_path
        if script_form.diagram_type.data == 1:
            script_form.diagram_path.data = painter.draw_graph(script_content)
        elif script_form.diagram_type.data == 2:
            painter.set_directed(False)
            script_form.diagram_path.data = painter.draw_graph(script_content)
        else:
            script_form.diagram_path.data = painter.draw_uml(script_content)

        script_form.diagram_content.data = painter.content

        if script_form.save_button.data:

            diagram_id = script_form.diagram_id.data
            if diagram_id:
                diagram = Diagram.query.filter_by(diagram_id=diagram_id).first()
            else:
                diagram = Diagram()
            logger.info("save {}, {}".format(script_form.diagram_id.data, script_form.diagram_name.data))
            diagram.diagram_name = script_form.diagram_name.data
            diagram.diagram_script = script_form.script_content.data
            diagram.diagram_type = script_form.diagram_type.data
            diagram.image_path = script_form.diagram_path.data
            diagram.author_id = current_user.id
            tagName = script_form.diagram_tag.data
            tag = Tag.query.filter_by(name=tagName).first()
            if not tag:
                tag = Tag(name=tagName)
                db.session.add(tag)
                db.session.commit()

            diagram.tag_id = tag.id


            logger.info("save diagram {}".format(diagram))
            db.session.add(diagram)
            db.session.commit()

    else:
        logger.info(script_form.errors)
        #flash(script_form.errors, 'error')

    return render_template('diagram.html', form=script_form, upload_form=upload_form)
