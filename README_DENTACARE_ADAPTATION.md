# Enigma Dent — DentaCare adaptation

Це версія Enigma Dent, у якій frontend повністю переведений на адаптовану структуру безкоштовного шаблону DentaCare / Colorlib.

## Що залишено з Django-проєкту
- заявки на прийом і статуси в Django Admin;
- модерація відгуків;
- Telegram notification service;
- база даних і міграції;
- існуючі юридичні сторінки;
- маршрути терапії, пародонтології та ортопедії.

## Що замінено
- весь основний frontend;
- header / footer / hero;
- головна сторінка;
- сторінки послуг;
- форма запису;
- сторінка відгуку;
- контакти;
- стартова сторінка прайсу.

## Що видалено як зайве
- demo blog;
- demo doctors/staff pages;
- newsletter;
- demo USD pricing plans;
- старі fragments/components фронтенду;
- SCSS source tree та demo HTML DentaCare;
- зайві duplicate assets.

## Запуск локально
```powershell
cd root
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

Потім відкрийте http://127.0.0.1:8000/

## Наступний етап
Повний прайс доцільно винести в Django models/admin і додати імпорт XLSX/CSV.


## Документи та сертифікати
- `/license/` — ліцензія Enigma Dent з `static/dentacare/images/license.jpg`.
- `/certificates/` — галерея сертифікатів `c1.jpg`–`c11.jpg`.
- Обидві сторінки мають збільшення зображень без сторонніх JS-фреймворків.

- Сертифікати можна додавати/приховувати/сортувати через Django Admin → Сертифікати. Якщо база порожня, сторінка автоматично показує наявні `c1.jpg`–`c11.jpg`.
