# Generated by Django 4.1.5 on 2023-02-26 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_comment_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile'),
        ),
    ]
