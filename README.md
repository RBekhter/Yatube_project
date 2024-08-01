# Yatube_project
Социальная сеть блогеров

Yatube дает пользователям возможность создать учетную запись, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся записи

### Technologies
Python 3.9
Django 2.2.19
Django Rest Framework 3.12.4

### Run project on dev-mode
- install and activate virtual environment
- install relations in requirements.txt
pip install -r requirements.txt
- make migrations
python manage.py makemigrations
python manage.py migrate

- in manage.py directory run the command:
python3 manage.py runserver

### API Yatube
This API is designed based on the REST architecture
[More about API Yatube](Yatube/api/README.md)

### Author RBexter