from django.db import migrations, models


def create_stats(apps, schema_editor):
    apps.get_model('home', 'GoogleReviewStats').objects.get_or_create(pk=1)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_seed_current_prices'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleReviewStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Середній рейтинг Google')),
                ('total_review_count', models.PositiveIntegerField(default=0, verbose_name='Кількість відгуків Google')),
                ('google_maps_url', models.URLField(blank=True, max_length=500, verbose_name='Посилання на Google Maps')),
                ('last_sync_at', models.DateTimeField(blank=True, null=True, verbose_name='Остання синхронізація')),
                ('last_sync_status', models.CharField(default='waiting', max_length=24, verbose_name='Статус синхронізації')),
                ('last_sync_error', models.TextField(blank=True, verbose_name='Помилка синхронізації')),
            ],
            options={
                'verbose_name': 'Статистика Google-відгуків',
                'verbose_name_plural': 'Статистика Google-відгуків',
            },
        ),
        migrations.CreateModel(
            name='GoogleReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_review_id', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Google Review ID')),
                ('reviewer_name', models.CharField(default='Користувач Google', max_length=255, verbose_name="Ім'я автора")),
                ('reviewer_profile_photo_url', models.URLField(blank=True, max_length=1000, verbose_name='Фото автора')),
                ('star_rating', models.PositiveSmallIntegerField(db_index=True, default=5, verbose_name='Оцінка')),
                ('comment', models.TextField(blank=True, verbose_name='Текст відгуку')),
                ('create_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата відгуку')),
                ('update_time', models.DateTimeField(blank=True, null=True, verbose_name='Дата оновлення')),
                ('reply_comment', models.TextField(blank=True, verbose_name='Відповідь Enigma Dent')),
                ('reply_update_time', models.DateTimeField(blank=True, null=True, verbose_name='Дата відповіді')),
                ('is_visible', models.BooleanField(db_index=True, default=True, verbose_name='Показувати на сайті')),
                ('synced_at', models.DateTimeField(auto_now=True, verbose_name='Синхронізовано')),
                ('raw_json', models.JSONField(blank=True, default=dict, verbose_name='Сирі дані Google')),
            ],
            options={
                'verbose_name': 'Google-відгук',
                'verbose_name_plural': 'Google-відгуки',
                'ordering': ['-create_time', '-id'],
            },
        ),
        migrations.RunPython(create_stats, migrations.RunPython.noop),
    ]
