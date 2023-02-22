from django.db import models  # noqa F401


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)