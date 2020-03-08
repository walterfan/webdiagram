from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms import BooleanField, SelectField, FileField
from wtforms import HiddenField
from wtforms.validators import DataRequired, Length, Optional
import datetime

FLOW_SCRIPT_SAMPLE = """
start -> a
a -> b[label="yes"]
a -> c[label="no"]
b -> end
c -> end
"""


class UploadForm(FlaskForm):
    script_file = FileField('Upload Script', validators=[FileAllowed(['txt'])])
    submit_file = SubmitField('Upload')


class ScriptForm(FlaskForm):
    default_script = FLOW_SCRIPT_SAMPLE
    default_file_name = "diagram_{}.png".format(datetime.datetime.now().strftime('%Y%m%d'))
    script_content = TextAreaField('script', validators=[DataRequired(), Length(1, 8192)],
                                   default=default_script.strip(),
                                   render_kw={
                                       "class": "form-control",
                                       "rows": 10})
    diagram_type = SelectField('action',
                               choices=[(1, 'directed graph'),
                                        (2, 'undirected graph '),
                                        (3, 'uml diagram')],
                               render_kw={"class": "form-control"},
                               coerce=int,
                               validators=[Optional()])
    submit_button = SubmitField('Generate', render_kw={"class": "btn btn-primary"})

    diagram_name = StringField('diagram_name', validators=[DataRequired(), Length(1, 256)],
                               default=default_file_name, render_kw={"class": "form-control"})
    diagram_tag = StringField('diagram_tag', validators=[DataRequired(), Length(1, 256)],
                               default='diagram', render_kw={"class": "form-control"})
    diagram_path = HiddenField('diagram_path')
    diagram_content = HiddenField('diagram_content')
    diagram_id = HiddenField('diagram_id')

    load_button = FileField('load', render_kw={"class": "btn btn-primary"})
    save_button = SubmitField('Save', render_kw={"class": "btn btn-primary"})