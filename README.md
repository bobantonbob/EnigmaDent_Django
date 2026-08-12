# Enigma Dent

Django website for Enigma Dent.

## Main sections
- Home
- Services: therapy, periodontology, orthopedics
- Prices
- Online appointment requests
- Contacts and map
- License
- Certificates
- Reviews with moderation
- Django Admin
- Telegram notifications for new appointment requests

## Local start
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Environment variables are loaded from `.env`.
