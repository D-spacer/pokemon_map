import folium
import json


from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        if pokemon_entity.appeared_at < localtime() < pokemon_entity.disappeared_at:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    for pokemon in Pokemon.objects.all():
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        if pokemon_entity.appeared_at < localtime() < pokemon_entity.disappeared_at:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': requested_pokemon,
        'img_url': request.build_absolute_uri(requested_pokemon.pokemon.image.url),
        "previous_evolution": {
            "title_ru": requested_pokemon.children.first().title_ru,
            "pokemon_id": requested_pokemon.children.first().id,
            "img_url": requested_pokemon.children.first().image.url
        },
        "next_evolution": {
            "title_ru": requested_pokemon.children.first().title_ru,
            "pokemon_id": requested_pokemon.children.first().id,
            "img_url": requested_pokemon.children.first().image.url
        }
    }
                  )

