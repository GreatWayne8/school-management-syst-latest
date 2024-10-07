# Generated by Django 4.0.8 on 2024-10-07 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_office_assistant'),
        ('medicals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='doctor',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='doctors_phone_number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='hospital',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student'),
        ),
    ]
