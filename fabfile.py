from fabric import task
from fabric import Connection
import pprint
from app import app
from portal import mail
from portal.diagram.painter import Painter
from portal.auth.models import User, Role
import os
import hashlib
import base64

from dotenv import load_dotenv

from portal.email import send_email

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

pp = pprint.PrettyPrinter(indent=4)

DEFAULT_HOSTS = ["localhost"]

#withSudo="sudo "
def run_cmd(c, cmd, withSudo=""):
	print(withSudo + cmd)
	c.local(withSudo + cmd)

@task(hosts=DEFAULT_HOSTS)
def md5(message):
	m = hashlib.md5()
	m.update(message.encode('utf-8'))
	return m.digest()

@task(hosts=DEFAULT_HOSTS)
def base64_encode(message):
	return base64.b64encode(bytes(message, 'utf-8')).decode('utf-8')

@task(hosts=DEFAULT_HOSTS)
def base64_decode(message):
	return base64.b64decode(message).decode('utf-8')

@task(hosts=DEFAULT_HOSTS)
def dump_config(c):
	with app.app_context():
		pp.pprint(app.config)


@task(hosts=DEFAULT_HOSTS)
def init_db(c):
	run_cmd(c, 'flask db init')
	run_cmd(c, 'flask db migrate -m "init tables"')
	run_cmd(c, 'flask deploy')

@task(hosts=DEFAULT_HOSTS)
def upgrade_db(c):
	run_cmd(c, 'flask db migrate -m "update tables"')
	run_cmd(c, 'flask db upgrade')

@task(hosts=DEFAULT_HOSTS)
def runserver(c, port=5000):
	c.local("flask run --port  %s" % port)

@task(hosts=DEFAULT_HOSTS)
def list_user(c):
	with app.app_context():
		roles = Role.query.all()
		print("-" * 100)
		print("Role#id, name, default, permissions")
		print("-" * 100)
		for role in roles:
			print("{}".format(role))

		print("-" * 100)
		users = User.query.all()
		print('User#id, username, password_hash, email, name, confirmed, role_id')
		print("-"*100)
		for user in users:
			print("{}, {}, {}, {}, {}, {}, {}"
				  .format(user.id, user.username, user.password_hash, user.email, user.name, user.confirmed, user.role_id))

			diagrams = user.diagrams
			for diagram in diagrams:
				print("{}".format(diagram))

@task(hosts=DEFAULT_HOSTS)
def send_mail(c, recipient='fanyamin@hotmail.com', subject="Don't forget practice", body='Practice makes Perfect'):

	with app.app_context():
		sender = app.config['MAIL_SENDER']
		print("{} send email to {}".format(sender, recipient))
		msg = Message(subject, sender=sender, recipients=[recipient])
		msg.body = body
		msg.html = "<p>Dear Walter, </p><p>{}</p><p>Regards,<br/>Walter</p>".format(body)
		mail.send(msg)

@task(hosts=DEFAULT_HOSTS)
def draw_graph(script_file, image_file):
	painter = Painter(os.path.basename(image_file))
	painter.path = os.path.dirname(image_file)

	with open(script_file, 'r') as fp:
		script_content = fp.read()

	painter.draw_graph(script_content)

@task(hosts=DEFAULT_HOSTS)
def draw_uml(script_file, image_file):
	painter = Painter(os.path.basename(image_file))
	painter.path = os.path.dirname(image_file)

	with open(script_file, 'r') as fp:
		script_content = fp.read()

	painter.draw_uml(script_content)