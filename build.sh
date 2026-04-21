#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
<< END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='harshi').exists():
    User.objects.create_superuser('harshi', 'channelwebdev@gmail.com', 'QWERTY@098')
END