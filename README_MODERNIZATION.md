# Enigma Dent — модернізація сайту

## Що змінено

- Google Form повністю прибрана зі сторінки запису.
- Додана власна Django-форма запису з CSRF-захистом та валідацією телефону.
- Кожна заявка спочатку зберігається в базі даних, тому не губиться навіть якщо Telegram тимчасово недоступний.
- Після успішного збереження сайт надсилає адміністратору повідомлення через Telegram Bot API.
- Відгуки отримали модерацію: `Новий` → `Опублікований` / `Прихований`.
- На публічній сторінці показуються тільки схвалені відгуки.
- Django Admin перероблена під робочий CRM-подібний режим: статуси, фільтри, пошук, нотатки адміністратора, дати, IP та bulk-actions.
- Додані актуальні Telegram / Instagram / Facebook посилання.
- Збережена зелено-біла палітра Enigma Dent, але форма й інтерфейс стали сучаснішими та адаптивними.
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, Telegram credentials винесені в environment variables.
- Часовий пояс змінено на `Europe/Kyiv`, мова — `uk`.

## Telegram

1. У Telegram відкрийте `@BotFather` і створіть бота.
2. Додайте бота в чат або канал, куди повинні надходити заявки.
3. Заповніть `TELEGRAM_BOT_TOKEN` і `TELEGRAM_CHAT_ID` у змінних середовища.
4. Для публічного каналу `TELEGRAM_CHAT_ID` може бути username каналу (наприклад `@channelname`) за умови, що бот має право писати в нього. Для приватного чату використовуйте numeric chat id.

> `https://t.me/enigmadent` залишено як клієнтське посилання на Telegram Enigma Dent. Воно не є секретним Bot Token.

## Запуск після заміни файлів

```bash
python manage.py migrate
python manage.py createsuperuser   # якщо адміністратора ще немає
python manage.py collectstatic --noinput  # production
python manage.py runserver
```

Адмінка: `/admin/`

## Production

Рекомендовано використовувати актуальну підтримувану версію Django, HTTPS, `DEBUG=0`, окремий секретний ключ та production WSGI/ASGI server. Перед викладенням виконайте:

```bash
python manage.py check --deploy
```
