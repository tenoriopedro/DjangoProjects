# Deploy configuration

## Firsts steps

- Prepare local_settings.py
- Create your Ubuntu 20.04 LTS server

Command to generate SECRET_KEY

```
python -c "import string as s;from secrets import SystemRandom as SR;print(''.join(SR().choices(s.ascii_letters + s.digits + s.punctuation, k=64)));"
```
 
## Creating your ssh key

```
ssh-keygen -C 'USERNAME'
```

## On the Server

### Conecting

```
ssh user@ip_server
```

### Initial commands

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv -y

sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git -y

Creating project and repository folders

```
mkdir ~/agendarepo ~/agendaapp
```

Configuring repository

```
cd ~/agendarepo
git init --bare
cd ..
cd ~/agendaapp
git init
git remote add agendarepo ~/agendarepo
git add .
git commit -m 'Initial'
git push agendarepo main -u # error

On the server

```
cd ~/agendaapp
git pull agendarepo main
```

## Configuring postgresql

```
sudo -u postgresql psql 

postgres=# create role my_user with login superuser createdb createrole password 'my_password';
CREATE ROLE 
postgres=# create database agenda_db with owner my_user;
CREATE DATABASE 
postques=# grant all privileges on database agenda_db to my_user;
GRANT 
postgres=# \q

sudo systemctl restart postgresql
```

## Creating local_settings.py on the server

```
nano ~/agendaapp/project/local_settings.py
```

## Configuring Django on the server

```
cd ~/agendaapp
python3.11 -m venv venv
.venv/bin/activate
pip install --upgrade pip
pip install django
pip install pillow
pip install gunicorn
pip install psycopg
pip install faker

python manage.py runserver
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

```

## Allow larger files in nginx

```
sudo nano /etc/nginx/nginx.conf
```

Adicione me http {}:

```
client_max_body_size 30M;
```

```
sudo systemctl restart nginx
```