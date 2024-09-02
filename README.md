# Yatube_project
Социальная сеть блогеров

Yatube дает возможность пользователям создавать учетные записи, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся посты.

В процессе разработки я упражнялся с Django, Django ORM, Django REST Framework. С помощью библиотеки Unittest написаны тесты. При создании шаблонов были использованы HTML и CSS (Bootstrap).
С помощью библиотеки sorl-thumbnail реализована возможность добавлять картинки к постам.
В планах развернуть проект в docker-контейнере и разместить сервере

### Technologies
Python 3.9
Django 2.2.19
Django Rest Framework 3.12.4

### Run project on dev-mode
- Clone repository and go it on the command line:
git clone https://github.com/RBekhter/Yatube_project.git
cd Yatube_project
- install and activate virtual environment
- install relations in requirements.txt
pip install -r requirements.txt
- make migrations
python manage.py makemigrations
python manage.py migrate

- in manage.py directory run the command:
python3 manage.py runserver

### API Yatube
API is designed using the REST architecture
[More about API Yatube](Yatube/api/README.md)

### Author RBexter