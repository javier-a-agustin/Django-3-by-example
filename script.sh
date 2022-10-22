# Virtual env name: d3

# [ -d env ] || python -m venv env

# ./env/Scripts/activate

RUN pyenv activate d3

cd './Chapter 1 - 2 - 3'
cd './mysite'
python manage.py runserver

#pip install django==3.2.7
#pip freeze > requirements.txt
#django-admin startproject new_project

# read build

# echo $build
