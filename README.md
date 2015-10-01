# Team Interpreters 362 Project

## Requirements to install locally:

 - SublimeText 3 or PyCharm (or your favorite text editor) 
 - virtualenv
 - Python 3.4.3 
 - Git

## Requirements to install in our virtualenv:

 - Django 1.8

## Installation Instructions for Ubuntu 14.04 (or later)

### 1. Let's install Git:
    
 - Type the following:
	 - $ sudo apt-get update
	 - $ sudo apt-get upgrade
	 - $ sudo apt-get install git
 - Now we have git installed, create a directory for our project.
	 - cd into that directory from your terminal.
 - Now we're going to clone the project into your project directory.
	 - $ git clone https://github.com/SurajAnil/CPSC362-Project.git

### 2. Let's install Python 3.4.3:

 - Type the following commands:
	 - $ sudo apt-get install python3
 - After it's all completed, run the following to check the version:
	 - $ python3
 - This should open the Python3 interpreter and the version should say 3.4.3
	 - To exit the interpreter, do CTRL-D.
    
### 3. Let's install virtualenv:

 - $ sudo apt-get install virtualenv
 - Go to your project root directory and type:
	 - $ virtualenv -p python3 env
 - This creates a virtual environment where all the libraries and executables for our prject will live. This will help keep everything the same accross different machines.
 - Now to access the virtualenv, we do:
	 - $ source env/bin/activate
 - You'll notice that your shell has been prepended with "(env)", this indicates your in the environment. 
 - Note: To go back to your normal shell environment, do:
 	 - $ deactivate
 - Now we need to install our Django requirements:
 	 - cd into the project root folder, then proceed to next step.
	 	 - $ pip install -r requirements.txt
 - **That's it. Now your machine is setup with the development environment.**

## Superuser account for SQLite3 DB

 - Username: `root`
 - Password: `password`
 - Email: **Not using email address**

## Links:

 - http://tutorial.djangogirls.org/en/index.html
 - https://realpython.com/learn/start-django/#django-18
 - http://erwinyusrizal.me/create-django-17-python-34-webfaction/

##  Possible hosting solutions:

 - https://www.pythonanywhere.com/
