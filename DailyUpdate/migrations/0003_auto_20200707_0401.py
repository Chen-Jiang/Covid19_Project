# Generated by Django 3.0.7 on 2020-07-07 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailyUpdate', '0002_auto_20200622_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='confirm_img',
            field=models.FileField(null=True, upload_to='images/confirmed', verbose_name=''),
        ),
        migrations.AddField(
            model_name='country',
            name='daily_img',
            field=models.FileField(null=True, upload_to='images/daily', verbose_name=''),
        ),
    ]
