from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('home', '0005_alter_response_name_alter_response_timestamp')]

    operations = [
        migrations.CreateModel(
            name='PriceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('therapy', 'Терапія'), ('periodontology', 'Пародонтологія'), ('orthopedics', 'Ортопедія')], db_index=True, max_length=24, verbose_name='Напрям')),
                ('title', models.CharField(max_length=160, verbose_name='Категорія')),
                ('subtitle', models.CharField(blank=True, max_length=240, verbose_name='Пояснення')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показувати')),
            ],
            options={'verbose_name': 'Категорія прайсу', 'verbose_name_plural': 'Категорії прайсу', 'ordering': ['section', 'order', 'id']},
        ),
        migrations.CreateModel(
            name='PriceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, verbose_name='Код')),
                ('name', models.CharField(max_length=320, verbose_name='Послуга')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Ціна, грн')),
                ('price_text', models.CharField(blank=True, help_text='Напр.: «безкоштовно», «від 1700 грн». Якщо порожньо — показується числова ціна.', max_length=80, verbose_name='Текст ціни')),
                ('note', models.CharField(blank=True, max_length=240, verbose_name='Примітка')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показувати')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='home.pricecategory', verbose_name='Категорія')),
            ],
            options={'verbose_name': 'Позиція прайсу', 'verbose_name_plural': 'Позиції прайсу', 'ordering': ['category__section', 'category__order', 'order', 'id']},
        ),
    ]
