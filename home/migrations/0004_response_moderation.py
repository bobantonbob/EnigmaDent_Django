from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('home', '0003_response_image')]

    operations = [
        migrations.AlterField(model_name='response', name='email', field=models.EmailField(blank=True, max_length=100, verbose_name='Email')),
        migrations.AlterField(model_name='response', name='image', field=models.FileField(blank=True, null=True, upload_to='images/response_user', verbose_name='Фото')),
        migrations.AlterField(model_name='response', name='response', field=models.TextField(max_length=2000, verbose_name='Відгук')),
        migrations.AddField(model_name='response', name='status', field=models.CharField(choices=[('new', 'Новий'), ('approved', 'Опублікований'), ('hidden', 'Прихований')], db_index=True, default='approved', max_length=16, verbose_name='Модерація'), preserve_default=False),
        migrations.AlterField(model_name='response', name='status', field=models.CharField(choices=[('new', 'Новий'), ('approved', 'Опублікований'), ('hidden', 'Прихований')], db_index=True, default='new', max_length=16, verbose_name='Модерація')),
        migrations.AddField(model_name='response', name='admin_note', field=models.TextField(blank=True, verbose_name='Нотатка адміністратора')),
        migrations.AddField(model_name='response', name='source', field=models.CharField(default='website', max_length=32, verbose_name='Джерело')),
        migrations.AddField(model_name='response', name='ip_address', field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
        migrations.AlterModelOptions(name='response', options={'ordering': ['-timestamp'], 'verbose_name': 'Відгук', 'verbose_name_plural': 'Відгуки'}),
    ]
