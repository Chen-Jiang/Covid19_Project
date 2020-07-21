from django.db import models


# Create your models here.
class Country(models.Model):
    fullName = models.CharField(max_length=80, unique=False)
    shortName = models.CharField(max_length=30, unique=False)
    continent = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField('DATE')
    total_case = models.FloatField(blank=True, null=True)
    new_case = models.FloatField(blank=True, null=True)
    total_death = models.FloatField(blank=True, null=True)
    new_death = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.fullName


class DailySituation(models.Model):
    name = models.CharField(max_length=80, unique=True)
    date = models.DateField('DATE')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    # confirm_img = models.BinaryField(upload_to='images/confirmed', null=True, verbose_name="")
    # confirm_img = models.ImageField(upload_to='images/confirm/', default='con.png')
    # daily_img = models.ImageField(upload_to='images/daily/', default='daily.png')
    confirm_img = models.BinaryField()
    daily_img = models.BinaryField()

    def __str__(self):
        return self.name
