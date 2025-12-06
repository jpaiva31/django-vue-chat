#!/bin/sh

echo "🚀 Entrypoint iniciado..."

# Exit on error
set -e

echo "⏳ Aguardando o Postgres..."
until nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo "🔄 Aguardando banco em $DATABASE_HOST:$DATABASE_PORT..."
  sleep 1
done

echo "✅ Banco disponível!"

echo "📌 Criando migrations..."
python manage.py makemigrations --noinput

echo "📌 Rodando migrations..."
python manage.py migrate --noinput

echo "📌 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando Gunicorn..."
exec gunicorn realmate_challenge.asgi:application \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:80 \
    --workers 2
