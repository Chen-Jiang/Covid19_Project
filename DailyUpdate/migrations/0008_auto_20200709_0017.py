# Generated by Django 3.0.7 on 2020-07-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailyUpdate', '0007_remove_dailysituation_daily_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysituation',
            name='confirm_img',
            field=models.ImageField(default='img.png', upload_to='images'),
        ),
    ]
