from django.db import models  # noqa F401


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Pokemon(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
