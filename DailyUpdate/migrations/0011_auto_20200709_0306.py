# Generated by Django 3.0.7 on 2020-07-09 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DailyUpdate', '0010_auto_20200709_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailysituation',
            name='confirm_img',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='dailysituation',
            name='daily_img',
            field=models.BinaryField(),
        ),
    ]
