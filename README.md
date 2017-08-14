This is a simple tutorial for this project

At first clone this project to your local machine git clone https://github.com/evheniyonoshko/leaderonomics.git

Than go to the project dir ('cd leaderonomics'), create virtualenv, and install requirements.txt ("pip install -r requirements.txt")

Then create postgresql database and put database settings to settings.py of this project:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'user_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

And you need also put your smpt settings in settings.py file, if you does not changed it, your email notification will not work:

DEFAULT_FROM_EMAIL = 'server_email' # need be changed
SERVER_EMAIL = 'server_email' # need be changed
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'server_email' # need be changed
EMAIL_HOST_PASSWORD = 'email_password' # need be changed

All endpoints:

1. 
For singin, you need POST singin data(email, password, first_name, last_name, passport_number)
to url http://localhost:8000/api-auth/singin/
2. 
For login, you need POST singin data(email, password)
to url http://localhost:8000/api-auth/login/
3. 
For logout, you need GET http://localhost:8000/api-auth/logout/
4. 
Menegers can get all pending clients, GET http://localhost:8000/api/v1.0/accounts/pending/
5. 
Menegers can activate pending clients one by one, PUT {'is_active': True} http://localhost:8000/api/v1.0/accounts/pending/{id}
6. 
Menegers can get all closed clients, GET http://localhost:8000/api/v1.0/accounts/closed/
7.
Menegers can delete all closed clients, DELETE http://localhost:8000/api/v1.0/accounts/closed/{id}
8.
When clients singin, menegers get email notification(like "You have new accounts that need activate")
9.
When menegers activate client account, client get email notification(like "Your account is activated")
10.
When menegers delete client account, client get email notification(like "Your account was deleted")
11.
You can create menegers in admin menu (as superuser) http://localhost:8000/admin/