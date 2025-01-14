import folium
import json


from django.utils.timezone import localtime
from django.shortcuts import render, get_object_or_404
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
    local_time = localtime()
    for pokemon_entity in PokemonEntity.objects.exclude(disappeared_at__lte=local_time,
                                                        appeared_at__gte=local_time):
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
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.exclude(disappeared_at__lte=local_time,
                                                        appeared_at__gte=local_time,
                                                        pokemon=requested_pokemon):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    serialized_previous = {
        "title_ru": requested_pokemon.children.first().title_ru,
        "pokemon_id": requested_pokemon.children.first().id,
        "img_url": requested_pokemon.children.first().image.url
    }
        
    serialized_next =  {
        "title_ru": requested_pokemon.children.first().title_ru,
        "pokemon_id": requested_pokemon.children.first().id,
        "img_url": requested_pokemon.children.first().image.url
    }
        
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': requested_pokemon,
        'img_url': request.build_absolute_uri(requested_pokemon.pokemon.image.url),
        "previous_evolution": serialized_previous,
        "next_evolution": serialized_next
    }
                 )

