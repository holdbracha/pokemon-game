import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

def get_pokemons_by_trainer(trainer_name):
    with connection.cursor() as cursor:
        query = """SELECT pokemon.name 
            FROM pokemon join pokemon_owner on pokemon.id = pokemon_owner.pokemon_id join owner on owner.id=pokemon_owner.owner_id 
            WHERE owner.name= '{}'""".format(trainer_name)
        cursor.execute(query)
        result = []
        for c in cursor.fetchall():
            result.append(c["name"])
        return result


def get_trainers_of_pokemon(pokemon_name):
    with connection.cursor() as cursor:
        query = """SELECT owner.name
                    FROM pokemon join pokemon_owner on pokemon.id = pokemon_owner.pokemon_id 
                    join owner on owner.id=pokemon_owner.owner_id 
                    WHERE pokemon.name= '{}'""".format(pokemon_name)
        cursor.execute(query)
        result = []
        for c in cursor.fetchall():
            result.append(c["name"])
        return (result)