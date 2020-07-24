#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "EntryPointを読み込み"
echo $DJANGO_SETTINGS_MODULE

#python3 manage.py flush --no-input
python3 manage.py migrate
python3 manage.py collectstatic --no-input --clear
#cd config
#python3 manage.py shell
#python3 -V
#テストデータを実行したい
pwd

#python3 test_data/make_data.py
echo "from config.test_data.make_data import main; main()" | python3 manage.py shell

echo "from django.contrib.auth.models import User; User.objects.create_superuser('chiaki', 'admin@example.com', 'chiaki1990')" | python3 manage.py shell

exec "$@"