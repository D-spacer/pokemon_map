from django.db import models  # noqa F401


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Pokemon(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='images')
    title_ru = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    child = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name='children')
    objects = models.Manager()

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.DO_NOTHING, related_name='entities')
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
    objects = models.Manager()
