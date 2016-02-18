set -e
python manage.py initdb_demo --noinput --traceback
python manage.py garble_persons --distribution=ee



