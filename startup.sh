#source ./venv/bin/activate
export FLASK_DEBUG=1
export FLASK_APP=app.py

if [ $# -eq 0 ]  # Must have command-line args to demo script.
then
  echo "Please invoke this script with one or more command-line arguments."
  flask run --host=0.0.0.0 --port=8000
else
  flask run --host=0.0.0.0 --port=$1
fi

