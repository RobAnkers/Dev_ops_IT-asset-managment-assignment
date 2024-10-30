# Digital & Technology Solutions
#     Degree Apprenticeship

Software Engineering & Agile (QAC020N227S)
Assignment March 22, 2024

Rob Ankers





# Getting started

## Requirements:
    - [python](https://www.python.org)

## Windows
    - create the virtual environment: `virtualenv env`
    - start the virtual environment: `.env\scripts\activate`
    - install dependencies: `pip install -r requirements.txt`


## Mac
    - setup a virtual environment: `python3 -m venv env`
    - start the virtual environment: `source .venv/scripts/activate`
    - install django: `pip3 install django`
    - run the web app: `python3 manage.py runserver`



## Resources
    - [“How-to” guides] (https://docs.djangoproject.com/en/5.0/howto/)
    - [VSCode Guide to Django](https://code.visualstudio.com/docs/python/tutorial-django)

## Dependency management
    - perform the following steps while the virtual environment is active.
    - whenever a new dependency is added generate a new dependency list using
    `pip freeze > requirements.txt` and push changes.
    - When a dependency has been added by another user, pull main and install
    dependencies using `pip install -r requirements.txt`
    - By doing this everyone's virtual environment will remain up to date.

## Useful Information
    - Admin account - username admin, password admin
    - Admin screen - 127.0.0.1/admin


