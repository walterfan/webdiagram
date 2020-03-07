

# environment prepare

```

brew install libev
brew install python3

virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
source setenv.sh
```


# DB migration

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