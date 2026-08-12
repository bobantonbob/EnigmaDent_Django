from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Сертифікат Enigma Dent', max_length=180, verbose_name='Назва')),
                ('issuer', models.CharField(blank=True, max_length=180, verbose_name='Організатор / навчальний центр')),
                ('issued_at', models.DateField(blank=True, null=True, verbose_name='Дата отримання')),
                ('image', models.FileField(upload_to='certificates/', verbose_name='Зображення сертифіката')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показувати на сайті')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Додано')),
            ],
            options={
                'verbose_name': 'Сертифікат',
                'verbose_name_plural': 'Сертифікати',
                'ordering': ['order', '-issued_at', '-created_at'],
            },
        ),
    ]
