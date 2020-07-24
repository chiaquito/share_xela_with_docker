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
python3 manage.py makemigrations --settings config.settings.dev_settings
python3 manage.py migrate --settings config.settings.dev_settings

#echo "from config.set_up import main; main()" | python3 manage.py shell
echo "from config.test_data.make_data import main; main()" | python3 manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('chiaki', 'admin@example.com', 'chiaki1990')" | python3 manage.py shell

exec "$@"
