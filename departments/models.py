from django.db import models


class Articles(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Нова'
        CONTACTED = 'contacted', 'Зв’язались'
        CONFIRMED = 'confirmed', 'Запис підтверджено'
        DONE = 'done', 'Завершено'
        CANCELLED = 'cancelled', 'Скасовано'

    title = models.CharField("Ім'я", max_length=100)
    about = models.CharField('Послуга / причина звернення', max_length=256)
    email = models.EmailField('Email', max_length=120, blank=True)
    phone = models.CharField('Телефон', max_length=30)
    message = models.TextField('Повідомлення', max_length=2000, blank=True)
    preferred_time = models.CharField('Бажаний час', max_length=120, blank=True)
    status = models.CharField('Статус', max_length=16, choices=Status.choices, default=Status.NEW, db_index=True)
    admin_note = models.TextField('Нотатка адміністратора', blank=True)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)
    source = models.CharField('Джерело', max_length=32, default='website')
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на прийом'
        verbose_name_plural = 'Заявки на прийом'

    def __str__(self):
        return f'{self.title} — {self.phone}'


class ResponseSite(models.Model):
    title = models.CharField("Ім'я", max_length=100)
    about = models.TextField('Тема', max_length=256)
    message = models.TextField('Повідомлення', max_length=1024)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Повідомлення з сайту'
        verbose_name_plural = 'Повідомлення з сайту'

    def __str__(self):
        return self.title
