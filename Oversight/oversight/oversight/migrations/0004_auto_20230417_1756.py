# Generated by Django 3.2.9 on 2023-04-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oversight', '0003_rename_password_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='questions',
            field=models.TextField(blank=True),
        ),
    ]
