from django.db import models


class Response(models.Model):
    class ModerationStatus(models.TextChoices):
        NEW = 'new', 'Новий'
        APPROVED = 'approved', 'Опублікований'
        HIDDEN = 'hidden', 'Прихований'

    name = models.CharField("Ім'я", max_length=100)
    email = models.EmailField('Email', max_length=100, blank=True)
    response = models.TextField('Відгук', max_length=2000)
    image = models.FileField('Фото', upload_to='images/response_user', blank=True, null=True)
    timestamp = models.DateTimeField('Час', auto_now_add=True)
    status = models.CharField('Модерація', max_length=16, choices=ModerationStatus.choices,
                              default=ModerationStatus.NEW, db_index=True)
    admin_note = models.TextField('Нотатка адміністратора', blank=True)
    source = models.CharField('Джерело', max_length=32, default='website')
    ip_address = models.GenericIPAddressField('IP', blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

    def __str__(self):
        return f'{self.name} — {self.get_status_display()}'


class PriceCategory(models.Model):
    class Section(models.TextChoices):
        THERAPY = 'therapy', 'Терапія'
        PERIODONTOLOGY = 'periodontology', 'Пародонтологія'
        ORTHOPEDICS = 'orthopedics', 'Ортопедія'

    section = models.CharField('Напрям', max_length=24, choices=Section.choices, db_index=True)
    title = models.CharField('Категорія', max_length=160)
    subtitle = models.CharField('Пояснення', max_length=240, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показувати', default=True)

    class Meta:
        ordering = ['section', 'order', 'id']
        verbose_name = 'Категорія прайсу'
        verbose_name_plural = 'Категорії прайсу'

    def __str__(self):
        return f'{self.get_section_display()} — {self.title}'


class PriceItem(models.Model):
    category = models.ForeignKey(PriceCategory, on_delete=models.CASCADE, related_name='items', verbose_name='Категорія')
    code = models.CharField('Код', max_length=20, blank=True)
    name = models.CharField('Послуга', max_length=320)
    price = models.DecimalField('Ціна, грн', max_digits=10, decimal_places=2, blank=True, null=True)
    price_text = models.CharField('Текст ціни', max_length=80, blank=True, help_text='Напр.: «безкоштовно», «від 1700 грн». Якщо порожньо — показується числова ціна.')
    note = models.CharField('Примітка', max_length=240, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показувати', default=True)

    class Meta:
        ordering = ['category__section', 'category__order', 'order', 'id']
        verbose_name = 'Позиція прайсу'
        verbose_name_plural = 'Позиції прайсу'

    def __str__(self):
        return f'{self.code} {self.name}'.strip()

    @property
    def display_price(self):
        if self.price_text:
            return self.price_text
        if self.price is None:
            return 'Уточнюйте'
        value = int(self.price) if self.price == int(self.price) else self.price
        return f'{value} грн'


class GoogleReviewStats(models.Model):
    """Cached Google Business Profile rating summary for Enigma Dent."""
    average_rating = models.DecimalField('Середній рейтинг Google', max_digits=3, decimal_places=2, blank=True, null=True)
    total_review_count = models.PositiveIntegerField('Кількість відгуків Google', default=0)
    google_maps_url = models.URLField('Посилання на Google Maps', blank=True, max_length=500)
    last_sync_at = models.DateTimeField('Остання синхронізація', blank=True, null=True)
    last_sync_status = models.CharField('Статус синхронізації', max_length=24, default='waiting')
    last_sync_error = models.TextField('Помилка синхронізації', blank=True)

    class Meta:
        verbose_name = 'Статистика Google-відгуків'
        verbose_name_plural = 'Статистика Google-відгуків'

    def __str__(self):
        if self.average_rating is None:
            return 'Google Reviews — очікує синхронізації'
        return f'Google {self.average_rating} ★ · {self.total_review_count} відгуків'


class GoogleReview(models.Model):
    """Local copy of a review from the verified Enigma Dent Google Business Profile."""
    google_review_id = models.CharField('Google Review ID', max_length=255, unique=True, db_index=True)
    reviewer_name = models.CharField("Ім'я автора", max_length=255, default='Користувач Google')
    reviewer_profile_photo_url = models.URLField('Фото автора', blank=True, max_length=1000)
    star_rating = models.PositiveSmallIntegerField('Оцінка', default=5, db_index=True)
    comment = models.TextField('Текст відгуку', blank=True)
    create_time = models.DateTimeField('Дата відгуку', blank=True, null=True, db_index=True)
    update_time = models.DateTimeField('Дата оновлення', blank=True, null=True)
    reply_comment = models.TextField('Відповідь Enigma Dent', blank=True)
    reply_update_time = models.DateTimeField('Дата відповіді', blank=True, null=True)
    is_visible = models.BooleanField('Показувати на сайті', default=True, db_index=True)
    synced_at = models.DateTimeField('Синхронізовано', auto_now=True)
    raw_json = models.JSONField('Сирі дані Google', default=dict, blank=True)

    class Meta:
        ordering = ['-create_time', '-id']
        verbose_name = 'Google-відгук'
        verbose_name_plural = 'Google-відгуки'

    def __str__(self):
        return f'{self.reviewer_name} — {self.star_rating}★'

    @property
    def stars(self):
        return '★' * max(0, min(5, int(self.star_rating or 0)))
