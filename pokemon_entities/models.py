from django.db import models  # noqa F401


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class Pokemon(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    title_ru = models.CharField(max_length=200, verbose_name='Русское название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Английское название')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Японское название')
    description = models.TextField(blank=True, verbose_name='Описание')
    child = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name='children', , verbose_name='Предыдущая эволюция')
    objects = models.Manager()

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    lat = models.FloatField(null=True, verbose_name='Широта')
    lon = models.FloatField(null=True, verbose_name='Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.DO_NOTHING, related_name='entities')
    appeared_at = models.DateTimeField(null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')
    objects = models.Manager()
    
    def __str__(self):
        return self.pokemon.title_ru
