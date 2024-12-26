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
