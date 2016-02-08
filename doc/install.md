instalacion de bd (debian based):
```
$ sudo apt-get install postgresql postgresql-contrib
```
dependencias para pip psycopg2:
```
sudo apt-get install libpq-dev python-dev
```
installar psycopg2 en venv respectivo
```
pip install psycopg2
```
crear usuario y db
```
user@local:~$ sudo su - postgres
postgres@local:~$ createdb mydb
$ createuser -P username
    username
    pass
    pass
    n
    n
    n
$ psql
> GRANT ALL PRIVILEGES ON DATABASE mydb TO username;
```
probar
```
$ psql --dbname=megafrut --username=megafrut --host=localhost
```
configurar conexion sqlalchemy
```
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://username:pass@localhost/mydb'
```


instalación paquetes en distro (debian based):
```
$ sudo apt-get install git
$ sudo apt-get install nginx-full
$ sudo apt-get install python-pip
$ sudo apt-get install python-dev
$ sudo pip install uWSGI
$ sudo pip install virtualenv
```

clonar repo:
```
$ sudo mkdir -p /mnt/development/imatec
$ cd /mnt/development/imatec
$ git clone https://mvaldes@bitbucket.org/imatec/massaman.git
...
```

link simbólico para host de nginx:
```
$ sudo mkdir -p /www/localhost_massaman
$ cd /www/localhost_massaman
$ sudo ln -s /mnt/development/imatec/massaman/src src
```

crear ambiente virtual para la app. e instalar modulos:
```
$ cd /mnt/development/imatec/massaman/src/
$ virtualenv venv
$ source venv/bin/activate
(venv)$ pip install -r stable-req.txt
$ deactivate
...
si fallara la instalacion de algunos paquetes por dependencias:
- reportlab / Pillow -> sudo apt-get build-dep python-imaging --fix-missing
- psycopg2 -> sudo apt-get install libpq-dev


configurar virtualhost en nginx, editando /etc/nginx/sites-available/default o creando uno nuevo. hacer link simbólico a sites-enabled
```
server {
        listen 80;
        server_name massaman.local;

        location / {
                try_files $uri @flask;
        }

        location @flask {
                include uwsgi_params;
                uwsgi_pass unix:/www/localhost_massaman/src/massaman.sock;
                uwsgi_param UWSGI_PYHOME /www/localhost_massaman/src/venv;
                uwsgi_param UWSGI_CHDIR /www/localhost_massaman/src;
                uwsgi_param UWSGI_MODULE uwsgi_app_factory;
                uwsgi_param UWSGI_CALLABLE application;
        }
}
```

editar rutas en uwsgi_app_factory.py:
```
$ cd /www/localhost_massaman/src
$ sudo nano uwsgi_app_factory.py
```
editar las variables:
```
this_app_dir = "/www/localhost_massaman/src/"
activate_this = "/www/localhost_massaman/src/venv/bin/activate_this.py"
```

crear socket (si no existe) y asignar permisos:
```
$ cd /www/localhost_massaman/src
$ sudo uwsgi -s massaman.sock
CTRL^C
$ sudo chmod 660 massaman.sock
$ sudo chgrp www-data massaman.sock
```

copiar init script de uwsgi:
```
$ sudo cp /www/localhost_massaman/src/srv/massaman /etc/init.d/massaman
```
y modificar algunas variables, por ej:
```
PATH=/opt/uwsgi:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/uwsgi
LOG=/tmp/massaman.log
OWNER=root
GROUP=www-data
CHDIR=/www/localhost_massaman/src
```
daemon set to /usr/bin/uwsgi , si uwsgi se instala por pip este existirá en /usr/local/bin/uwsgi, crear link simbólico:
```
$ cd /usr/bin/
$ sudo ln -s /usr/local/bin/uwsgi uwsgi
```
instalar script para que inicie en boot 
```
# update-rc.d massaman defaults
```