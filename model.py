import pymysql
from request_pokemon_api import get_types_by_name, get_evolved_name


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
            FROM pokemon join pokemon_owner on pokemon.id = pokemon_owner.pokemon_id join owner 
            on owner.id=pokemon_owner.owner_id WHERE owner.name= '{}'""".format(trainer_name)
        cursor.execute(query)
        result = []
        for c in cursor.fetchall():
            result.append(c["name"])
        print(cursor.fetchall())
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
        return result


def get_city_id(city):
    with connection.cursor() as cursor:
        query = "SELECT id FROM city WHERE name= '{}'".format(city)
        cursor.execute(query)
        result = cursor.fetchone()
        return result.get("id")


def add_city(city):
    with connection.cursor() as cursor:
        query = "INSERT INTO city VALUES(default, '{}')".format(city)
        cursor.execute(query)
        connection.commit()


def owner_exists(name):
    with connection.cursor() as cursor:
        query = "SELECT id FROM owner WHERE name= '{}'".format(name)
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def add_trainer(name, city):
    city_id = get_city_id(city)

    if not city_id:
        add_city(city)
        city_id = get_city_id(city)

    if not owner_exists(name):
        with connection.cursor() as cursor:
            query = "INSERT INTO owner VALUES(default, '{}', {} )".format(name, city_id)
            cursor.execute(query)
            connection.commit()


#######################################################################

def get_pokemon_by_name(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * from pokemon where name = '{}'".format(pokemon_name)
            cursor.execute(query)
            result = cursor.fetchone()
            print("get_pokemon_by_name", pokemon_name)
            print(result)
            if not result:
                return 404

            return result
    except pymysql.err.IntegrityError as e:
        return 500


def get_pokemon_id_by_name(pokemon_name):
    with connection.cursor() as cursor:
        query = "SELECT id from pokemon where name = '{}'".format(pokemon_name)
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return None
        pokemon_id = result["id"]
        print("pokemon_id", pokemon_id)
        return pokemon_id


def update_types_using_name(pokemon_name, type_list):
    try:
        pokemon_id = get_pokemon_id_by_name(pokemon_name)
        with connection.cursor() as cursor:
            for type_ in type_list:
                print("type: ", type_)
                query = "SELECT id from types where type = '{}'".format(type_)
                cursor.execute(query)
                result = cursor.fetchone()
                type_id = result["id"]
                print("type_id: ", type_id)
                query = "SELECT COUNT(*) FROM pokemon_type WHERE " \
                        "pokemon_id = {} and type_id = {}".format(pokemon_id, type_id)
                cursor.execute(query)
                result = cursor.fetchone()
                if not result['COUNT(*)']:
                    print("inserting...")
                    query = "INSERT INTO pokemon_type VALUES(null, {}, {})".format(type_id, pokemon_id)
                    cursor.execute(query)
                    connection.commit()
        return None
    except pymysql.err.IntegrityError as e:
        return 500


def update_types_and_get_pokemon_by_name(pokemon_name):
    result = get_pokemon_by_name(pokemon_name)
    if type(result) == int:  # THIS IS AN ERROR
        return result

    type_list = get_types_by_name(pokemon_name)
    error_code = update_types_using_name(pokemon_name, type_list)
    if error_code is not None:
        return error_code
    result["types"] = type_list
    return result


def evolve_pokemon_of_trainer(pokemon_name, trainer_name):
    next_stage_name = get_evolved_name(pokemon_name)
    if not next_stage_name:
        return 1

    # remove entry from pokemon_trainer:
    try:
        pok_id = get_pokemon_id_by_name(pokemon_name)
        if pok_id is None:
            return 2
        next_stage_id = get_pokemon_id_by_name(next_stage_name)
        if next_stage_id is None:
            return 3
        with connection.cursor() as cursor:
            query = "SELECT id from owner where name = '{}'".format(trainer_name)
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return 4
            trainer_id = result["id"]
            query = """SELECT COUNT(*) FROM pokemon_owner where pokemon_id = {} 
            and owner_id = {}""".format(pok_id, trainer_id)
            cursor.execute(query)
            result = cursor.fetchone()
            print("result:", result)
            if not result['COUNT(*)']:
                return 5
            query = """DELETE FROM pokemon_owner where pokemon_id = {} 
            and owner_id = {}""".format(pok_id, trainer_id)
            cursor.execute(query)
            connection.commit()
            query = "INSERT INTO pokemon_owner VALUES({}, {})".format(next_stage_id, trainer_id)
            cursor.execute(query)
            connection.commit()
            return next_stage_name
    except pymysql.err.IntegrityError as e:
        return 500

