until nc -z localhost 3306 || nc -z db 3306; do
    echo "waiting for database to start..."
    sleep 1
done

export GO_SECRET_KEY=$(dd if=/dev/urandom count=100 | tr -dc "A-Za-z0-9" | fold -w 60 | head -n1 2>/dev/null)
python3 go/manage.py flush --no-input
python3 go/manage.py makemigrations
python3 go/manage.py makemigrations go
python3 go/manage.py migrate
python3 go/manage.py createsuperuser --noinput --username=$superuser --email=$superuser$GO_EMAIL_DOMAIN
echo "from django.contrib.auth import get_user_model; User = get_user_model(); me = User.objects.get(username='$superuser'); me.first_name = 'David'; me.last_name = 'Haynes'; me.save(); " | python3 go/manage.py shell
python3 go/manage.py runserver 0.0.0.0:8000
