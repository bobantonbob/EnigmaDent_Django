from django.db import models


class Certificate(models.Model):
    title = models.CharField('Назва', max_length=180, default='Сертифікат Enigma Dent')
    issuer = models.CharField('Організатор / навчальний центр', max_length=180, blank=True)
    issued_at = models.DateField('Дата отримання', blank=True, null=True)
    image = models.FileField('Зображення сертифіката', upload_to='certificates/')
    description = models.TextField('Опис', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показувати на сайті', default=True)
    created_at = models.DateTimeField('Додано', auto_now_add=True)

    class Meta:
        ordering = ['order', '-issued_at', '-created_at']
        verbose_name = 'Сертифікат'
        verbose_name_plural = 'Сертифікати'

    def __str__(self):
        return self.title
