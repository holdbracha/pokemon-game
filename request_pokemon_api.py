import requests
import json


def get_types_by_name(pokemon_name):
    pokemon_url = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name + "/"
    res = requests.get(url=pokemon_url)
    pokemon_dict = res.json()
    extended_type_list = pokemon_dict.get("types")
    return [dict_["type"]["name"] for dict_ in extended_type_list]


def get_evolved_name(pokemon_name):
    pokemon_url = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name + "/"
    res = requests.get(url=pokemon_url)
    pokemon_dict = res.json()
    species_url = pokemon_dict["species"]["url"]
    res = requests.get(url=species_url)
    species_dict = res.json()
    chain_url = species_dict["evolution_chain"]["url"]
    res = requests.get(url=chain_url)
    evolution_chain_dict = res.json()
    dict_ = evolution_chain_dict.get("chain")
    evolution_chain = [dict_["species"]["name"]]
    while dict_.get("evolves_to"):
        dict_ = dict_["evolves_to"][0]
        evolution_chain.append(dict_["species"]["name"])

    for index, name in enumerate(evolution_chain):
        if name == pokemon_name:
            if index == len(evolution_chain) - 1:
                return None
            else:
                return evolution_chain[index + 1]


