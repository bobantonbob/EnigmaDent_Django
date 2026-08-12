from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [('departments', '0003_responsesite')]

    operations = [
        migrations.AlterField(model_name='articles', name='title', field=models.CharField(max_length=100, verbose_name="Ім'я")),
        migrations.AlterField(model_name='articles', name='about', field=models.CharField(max_length=256, verbose_name='Послуга / причина звернення')),
        migrations.AlterField(model_name='articles', name='email', field=models.EmailField(blank=True, max_length=120, verbose_name='Email')),
        migrations.AlterField(model_name='articles', name='phone', field=models.CharField(max_length=30, verbose_name='Телефон')),
        migrations.AlterField(model_name='articles', name='message', field=models.TextField(blank=True, max_length=2000, verbose_name='Повідомлення')),
        migrations.AddField(model_name='articles', name='preferred_time', field=models.CharField(blank=True, max_length=120, verbose_name='Бажаний час')),
        migrations.AddField(model_name='articles', name='status', field=models.CharField(choices=[('new', 'Нова'), ('contacted', 'Зв’язались'), ('confirmed', 'Запис підтверджено'), ('done', 'Завершено'), ('cancelled', 'Скасовано')], db_index=True, default='new', max_length=16, verbose_name='Статус')),
        migrations.AddField(model_name='articles', name='admin_note', field=models.TextField(blank=True, verbose_name='Нотатка адміністратора')),
        migrations.AddField(model_name='articles', name='created_at', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Створено'), preserve_default=False),
        migrations.AddField(model_name='articles', name='updated_at', field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, verbose_name='Оновлено'), preserve_default=False),
        migrations.AddField(model_name='articles', name='source', field=models.CharField(default='website', max_length=32, verbose_name='Джерело')),
        migrations.AddField(model_name='articles', name='ip_address', field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
        migrations.AddField(model_name='responsesite', name='created_at', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Створено'), preserve_default=False),
        migrations.AlterModelOptions(name='articles', options={'ordering': ['-created_at'], 'verbose_name': 'Заявка на прийом', 'verbose_name_plural': 'Заявки на прийом'}),
        migrations.AlterModelOptions(name='responsesite', options={'ordering': ['-created_at'], 'verbose_name': 'Повідомлення з сайту', 'verbose_name_plural': 'Повідомлення з сайту'}),
    ]
