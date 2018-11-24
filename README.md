source setup

python -m virtualenv venv 

source venv/bin/activate

pip install -r requirements.txt

flask init-db

flask run
