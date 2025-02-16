# YaTube_project: Социальная сеть блогеров
Yatube дает возможность пользователям создавать учетные записи, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся посты.
В процессе разработки использовал Django, делал запросы на Django ORM, Django REST Framework сделал API за меня😃. С помощью библиотеки Unittest написал тесты. Создал HTML-шаблоны, использовал CSS.
Упаковал проект и базу данных в docker-контейнеры

### Technologies
* Python 3.9
* Django 2.2.19
* Django Rest Framework 3.12.4
* PostgreSQL
* Docker

### Run project on dev-mode
- Clone repository:
git clone https://github.com/RBekhter/Yatube_project.git
- cd Yatube_project
- install and activate virtual environment
- install relations in requirements.txt:
pip install -r requirements.txt
- make migrations:
python manage.py makemigrations
python manage.py migrate
- in manage.py directory:
python3 manage.py runserver

* Docker is also available : docker pull rbexter/yatube_project

### API Yatube - (Yatube/api/README.md)

### Author rbexter