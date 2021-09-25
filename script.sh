[ -d env ] || python -m venv env

./env/Scripts/activate

cd './Chapter 1'
cd './mysite'
python manage.py runserver

#pip install django==3.2.7
#pip freeze > requirements.txt
#django-admin startproject new_project

# read build

# echo $build