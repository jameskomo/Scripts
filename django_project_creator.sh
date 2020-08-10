
#! /bin/bash

# SCRIPT DESCRIPTION

# This script creates a Python virtual environment with all the necessary packages,
#  before creating a new Django project and app, 
#  and starting a webserver to host the project.
# Create a new virtual environment and folder for this demo
# mkdir celery_demo 

## create the directory, -p means it will create parent dirs
## and not complain if the file already exists

DIR=$(pwd)
echo "Enter name of Django directory":
read filename
django_demo="$DIR/filename"
mkdir -p "$filename"
cd filename 
python3 -m venv myvenv 
source myvenv/bin/activate 

# install the necessary requirements via pip
python3 -m pip install --upgrade pip 
printf "celery==4.4.2\ncelery-progress==0.0.10\nDjango==3.0.6\nnasapy==0.2.6\npandas==1.0.3\npython-decouple==3.3\nrequests==2.23.0" >> requirements.txt 
python3 -m pip install -r requirements.txt 

# Create a new Django project and app 
django-admin startproject demo_project 
cd demo_project/ 
python3 manage.py startapp demo_app 

# Serve the new Django app
python3 manage.py runserver