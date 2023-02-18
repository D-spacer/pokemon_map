from django.db import models  # noqa F401


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()