virtualenv env -p python3.6

. env/bin/activate

pip install -r reqs.txt

./manage.py migrate
./manage.py runserver 8000

Visit browser under: http://127.0.0.1:8000/
