# Generated by Django 4.0.8 on 2024-09-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_lab_assistant',
            field=models.BooleanField(default=False),
        ),
    ]
