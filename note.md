174.138.31.75
ssh-keygen -t rsa
# django note
set up mac for django development environment --
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
                                            // install homebrew
    brew install python                     // install python
    pip3 install virtualenv                 // install virtualenv
now mkdir the project directory
    virtualenv ve                           //ve is the virtual environment we just created to further install django
    source ve/bin/activate                  // to activate virtualenv we just created
    pip3 install django                     // install django
    sudo ufw allow 8000                     // to allow port 8000 on
    django-admin startproject PROJECT_NAME  // create initial django project
    cd PROJECT_NAME
    python3 manage.py runserver             // to run localhost:8000 server
    python3 manage.py migrate               // to migrate the database system to django
    python3 manage.py createsuperuser       // to create to admin account for localhost:8000/admin
    python3 manage.py startapp APP_NAME     // to create app on django project
you are now ready to start developing the project.

@ project/urls.py; edit as below:
        from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('',include('system.urls'))
    ]

@ app/urls.py [CREATE NEW FILE and edit as below]
    from django.urls import path
    from .views import helloHome
    urlpatterns = [
        path('',helloHome)
    ]

@ app/views.py; edit as below:
    from django.shortcuts import render
    from django.http import HttpResponse

    def helloHome(request):
        return HttpResponse('<p>Yo! Whats up django</p>')       // test the urls route

@ project/settings.py; edit as below:
    INSTALLED_APPS:
        'system',                   // the app we just created above
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'system/template')],        // locate template file location

    @system/views.py; edit as below:
        from django.shortcuts import render
        from django.http import HttpResponse

        def HomePage(request):
            return render(request,'index.html')

//
{% block content%}
{% endblock content%}



##### Deploy on Ubuntu Server #####

sudo ufw allow 'OpenSSH'
sudo ufw status
sudo ufw app list

sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx curl
pip3 install virtualenv
source v/bin/activate
pip3 install django

sudo chmod -R 755 /PROJECT_DIRECTORY

#upload project

@ project's settings.py configure ALLOWED_HOSTS = ['localhost', 'server's ip']

sudo ufw allow 8000

# Test gunicorn is working by
gunicorn --bind 0.0.0.0:8000 LaBlog.wsgi
then visit server's ip at port 8000 to verify gunicorn do work!

sudo nano /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=la
Group=www-data
WorkingDirectory=/home/la/LaBlog/LaBlog
ExecStart=/home/la/LaBlog/v/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          LaBlog.wsgi:application

[Install]
WantedBy=multi-user.target

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl status gunicorn.socket

file /run/gunicorn.sock
# Out put as:
    /run/gunicorn.sock: socket

sudo systemctl status gunicorn

curl --unix-socket /run/gunicorn.sock localhost

sudo systemctl daemon-reload
sudo systemctl restart gunicorn

sudo nano /etc/nginx/sites-available/LaBlog

server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/la/LaBlog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/LaBlog /etc/nginx/sites-enabled

nginx -t

systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

### Django Image Field ###

first of all, install Python image library called 'Pillow':
    http://pillow.readthedocs.org/en/latest/installation.html
pip3 install pillow

@ project's settings.py add:

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

@ project's urls.py add

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
    	url(r'\^media/(?P<path>.\*)\$', 'django.views.static.serve',
    		{'document_root': settings.MEDIA_ROOT, }),
)


@ project's models.py add:

image = models.ImageField(upload_to="myrestaurants", blank=True, null=True)

upload image using forms.py by adding:

{% extends "myrestaurants/base.html" %}

{% block content %}

<form method="post" enctype="multipart/form-data" action="">
  {% csrf_token %}
  <table>
    {{ form.as_table }}
  </table>
  <input type="submit" value="Submit"/>
</form>

{% endblock %}

and below is how to fetch image from db as:

{% extends "myrestaurants/base.html" %}

{% block content %}

<h1>
  {{ dish.name }}
  {% if user == dish.user %}
    (<a href="{% url 'myrestaurants:dish_edit' dish.restaurant.id dish.id %}">edit</a>)
  {% endif %}
</h1>

<p>{{ dish.description }}</p>

{% if dish.image %}
  <p><img src="{{ dish.image.url }}"/></p>
{% endif %}

<p>Served by
  <a href="{% url 'myrestaurants:restaurant_detail' dish.restaurant.id %}">
    {{ dish.restaurant.name}}
  </a>
</p>

{% endblock %}

{% block footer %}
  Created by {{ dish.user }} on {{ dish.date }}
{% endblock %}

#####################################
# Django 5o Hours by Uncle Engineer #
#####################################
# EP 1

# EP 2

# EP 3

# EP 4

# EP 5

to create model for storing data

@ models.py
class AllProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    imageUrl = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):  # to show the name of products on database instead of object number
        return self.name

@terminal
python manage.py makemigrations
python manage.py migrate

to enable adding data to database add codes below
@ views.py
def AddProduct(request):
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageUrl = data.get('imageUrl')

        new = AllProduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imageUrl = imageUrl
        new.save()

    return render(request, 'myapp/addProduct.html')

# EP6
based | block | extends

# Reset admin password through python sheel

python manage.py shell
from djang.contrib.auth.models import User      #import User models
User.objects.all()                              #fetch user database
admin = User.objects.get(username='admin')      # .get use with unique value only
admin.set_password('xxxx')                      # xxxx is new password
admin.save()
quit()

# deploying to server
create digital ocean account
create droplet
create ssh key
    ssh-keygen -t rsa
ssh root@ip # ip from droplet creating on digital ocean
apt-get update && apt-get upgrade
hostnamectl set-hostname django-server
nano /etc/hosts
    add ip and hostname from above
sudo adduser picturaAdmin
sudo adduser picturaAdmin sudo
login
sudo apt-get install ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow 8000
sudo ufw allow 22
sudo ufw enable
sudo ufw status
sudo apt-get install python3-pip
sudo apt-get install python3-venv
sudo python3 -m venv venv
sudo chown -R 777 'venv'
sudo chmod -R 777 'venv'
source ./venv/bin/activate
pip -V
pip install --upgrade pip
pip install django==3.1.1
pip install pillow
check settings.py
  @ ALLOWED_HOSTS=[*]
  @ STATIC_ROOT = os.path.join(BASE_DIR, 'static')
sudo chown -R 777 'djangoWeb'
sudo chmod -R 777 'djangoWeb'
source ./venv/bin/activate
cd djangoWeb
python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
cd /etc/apache2/sites-available/
sudo cp 000.default.conf django_project.conf
sudo nano django_project.conf

Alias /static /home/picturaadmin/djangoWeb/static

<Directory /home/picturaadmin/djangoWeb/static>

    Require all granted

</Directory>


Alias /media /home/picturaadmin/djangoWeb/media

<Directory /home/picturaadmin/djangoWeb/media>

    Require all granted

</Directory>


<Directory /home/picturaadmin/djangoWeb/djangoWeb>

    <Files wsgi.py>

        Require all granted

    </Files>

</Directory>


WSGIScriptAlias / /home/picturaadmin/djangoWeb/djangoWeb/wsgi.py

WSGIDaemonProcess django_app python-path=/home/picturaadmin/djangoWeb python-home=/home/picturaadmin/venv

WSGIProcessGroup django_app

sudo a2ensite django_project.conf
sudo a2dissite 000-default.conf
cd /home/picturaadmin
sudo chown :www-data djangoWeb/db.sqlite3
sudo chmod 664 djangoWeb/db.sqlite3
sudo chown :www-data djangoWeb/
sudo chown -R :www-data djangoWeb/media
sudo chown -R 775 djangoWeb/media
sudo ufw delete allow 8000
sudo ufw allow http/tcp
sudo service apache2 restart

