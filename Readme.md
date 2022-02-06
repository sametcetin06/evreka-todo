# Evreka Todo Project

Project Setup
```
git clone 'project_url'
cd evreka-todo
virtualenv myvenv
```
Database Setup (Linux)
```
sudo -u postgres psql
create database evrekadb;
create user evrekauser with password 'evrekapassword';
grant all privileges on database evrekadb to evrekauser;
\q
```
Project Run
```
source myvenv/bin/active
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
open http://localhost:8000/schema
```
Settings Files
```
core/env/settings --> Project Settings
core/env/local    --> Local Environment
core/env/prod     --> Production Environment
JWT Token Prefix  --> JWT
```

Extras
 - JWT Token Authentication
 - Swagger
 - Log System