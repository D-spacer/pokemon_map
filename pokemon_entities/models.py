from django.db import models  # noqa F401


class Pokemon(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200)
# your models here
