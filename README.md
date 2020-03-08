# Introduction

This is an experimental web project when I'm learning flask by a flask book wrote by Miguel Grinberg.

The main functions of this project is to draw diagrams on web:

1. Flow chart
2. Mindmap
3. UML diagram: class diagram, sequence diagram, state diagram, etc.



# environment prepare

```

brew install libev
brew install python3

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
source setenv.sh
```

## create your environment file

```
# vi .env

FLASK_APP=app

MAIL_SERVER = smtp.163.com
MAIL_PORT = 465
MAIL_USE_SSL = true
MAIL_USE_TLS = false
MAIL_USERNAME = ***@163.com
MAIL_PASSWORD = ******
```

## DB migration

```

flask db init
flask db migrate -m "init tables"
flask db  upgrade
# upgrade and insert default roles
flask deploy
```


## flask shell

```
flask shell
>>> user = User.query.all()

```
# environment variables

.env for sensitive config
.flaskenv for public config

# FAQ
## how to start app?

```shell script
source ./venv/bin/activate
export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8000 &
```
## how to check schema

```shell script
sqlite3 web-diagram-dev.db
sqlite> .schema
sqlite> .quit 
```
