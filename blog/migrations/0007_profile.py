# Generated by Django 4.1.5 on 2023-02-12 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_pud_date_article_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('avatar', models.ImageField(upload_to='avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]