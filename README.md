source setup

python3 -m virtualenv venv 

source venv/bin/activate

pip3 install -r requirements.txt

flask init-db

flask run
