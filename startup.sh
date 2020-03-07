#source ./venv/bin/activate
export FLASK_DEBUG=1
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8000
