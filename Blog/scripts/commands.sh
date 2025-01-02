#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Esperar o banco de dados iniciar
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 3
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Esperar o banco de dados ficar completamente disponível
echo "🟡 Waiting for database to be available..."
sleep 10

# Criar banco de dados se não existir
echo "🟡 Checking if database '$POSTGRES_DB' exists..."
if ! PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -lqt | cut -d \| -f 1 | grep -qw $POSTGRES_DB; then
  echo "🟢 Database '$POSTGRES_DB' does not exist. Creating..."
  PGPASSWORD=$POSTGRES_PASSWORD createdb -h $POSTGRES_HOST -U $POSTGRES_USER $POSTGRES_DB
else
  echo "✅ Database '$POSTGRES_DB' already exists."
fi

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000