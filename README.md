# blogger-web
blogger-web project is built using [Django Framework](https://www.djangoproject.com/). It is a blogging platform for
people of Qaraqalpaqstan (or anyone who knows Qaraqalpaq language)

## Setup
### Initialize virtual environment
```
python3 -m venv blogger-web
cd blogger-web
source ./bin/activate
```
### Install required libraries
```
pip install -r requirements.txt
```
### Clone the project
```
git clone git@bitbucket.org:shagalalab/blogger-web.git
```
### Migrate DB
```
./manage.py migrate
```
### Run the app
```
./manage.py runserver
```
### Access the app
You can open the app in your browser by typing http://localhost:8000
