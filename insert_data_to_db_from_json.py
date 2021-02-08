import pymysql
import json

def connect_to_DB():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="bracha548",
        db="pokemon",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection



def insert_data(connection, city_table, owner, pokemon, types, pokemon_type, pokemon_owner):
    with connection.cursor() as cursor:
        for i in city_table:
            print("city:", i)
            query = "insert into city values ({}, '{}')".format(i[0], i[1])
            cursor.execute(query)
            connection.commit()
        for i in owner:
            print("owner:", i)
            query = "insert into owner values ({}, '{}', {})".format(i[0], i[1], i[2])
            cursor.execute(query)
            connection.commit()
        for i in pokemon:
            print("pokemon:", i)
            query = "insert into pokemon values ({}, '{}', {}, {})".format(i[0], i[1], i[2], i[3])
            cursor.execute(query)
            connection.commit()
        for id,i in enumerate(types):
            print("type:", id, i)
            query = "insert into types values ({}, '{}')".format(id, i)
            cursor.execute(query)
            connection.commit()
        for i in pokemon_type:
            print("pokemon_type:", i)
            query = "insert into pokemon_type values ({}, {}, {})".format(i[0], i[1], i[2])
            cursor.execute(query)
            connection.commit()
        for i in pokemon_owner:
            print("pokemon_owner:", i)
            query = "insert into pokemon_owner values ({}, {})".format(i[0], i[1])
            cursor.execute(query)
            connection.commit()

connection = connect_to_DB()

cities = {}

f = open('poke_data.json')
data = json.load(f)
city_id = 1
owner_id = 1
pokemon_type_id = 0
city = {}
owner = []
pokemon = []
pokemon_owner = []
types = []
pokemon_type = []
for pok in data:
    pokemon_type_id += 1
    pokemon.append([pok["id"], pok["name"], pok["height"], pok["weight"]])
    if pok["type"] not in types:
        types.append(pok["type"])
    type_id = types.index(pok["type"])   
    pokemon_type.append([pokemon_type_id, type_id, pok["id"]]) 
    for own in pok["ownedBy"]:
        if not city.get(own["town"]):
            city[own["town"]] = city_id
            city_id += 1
        t = False
        i = 0
        for o in owner:
            if o[1] == own["name"]:
                t = True
                i = o[0]
                break
        if not t:
            owner.append([owner_id,  own["name"], city[own["town"]]])
            i = owner_id
            owner_id += 1
        pokemon_owner.append([pokemon_type_id, i])
city_table = []
for k in city.keys():
    city_table.append([city[k], k])



connection = connect_to_DB()
insert_data(connection, city_table, owner, pokemon, types, pokemon_type, pokemon_owner)