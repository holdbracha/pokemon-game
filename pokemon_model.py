import json
import pymysql
from insert_data_to_db_from_json import *

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



def insert_data(connection):
    with connection.cursor() as cursor:
        for i in city_table:
            print("city:", i)
            query = "insert into city values ({}, '{}')".format(i[0], i[1])
            cursor.execute(query)
            connection.commit()
        for i in owner:
            print("owner:", i)
            query = "insert into owner values ({}, '{}', '{}')".format(i[0], i[1], i[2])
            cursor.execute(query)
            connection.commit()
        for i in pokemon:
            print("pokemon:", i)
            query = "insert into pokemon values ({}, '{}', '{}', {}, {})".format(i[0], i[1], i[2], i[3], i[4])
            cursor.execute(query)
            connection.commit()
        for i in pokemon_owner:
            print("pokemon_owner:", i)
            query = "insert into pokemon_owner values ('{}', '{}')".format(i[0], i[1])
            cursor.execute(query)
            connection.commit()

connection = connect_to_DB()

def get_haviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = "SELECT name FROM pokemon WHERE weight=(SELECT MAX(weight) FROM pokemon)"
            cursor.execute(query)
            result = cursor.fetchone()
            return result["name"]
    except:
        print("DB Error")
def findByType(type):
    try:
        with connection.cursor() as cursor:
            query = "SELECT name FROM pokemon WHERE type = '{}'".format(type)
            cursor.execute(query)
            result = []
            for c in cursor.fetchall():
                result.append(c["name"])

            return result
    except:
        print("DB Error")

def findOwners(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT owner.name FROM pokemon join pokemon_owner on pokemon.id = pokemon_owner.pokemon_id join owner on owner.id=pokemon_owner.owner_id WHERE pokemon.name= '{}'".format(pokemon_name)
            cursor.execute(query)
            result = []
            for c in cursor.fetchall():
                result.append(c["name"])
            return(result) 
    except:
        print("DB Error")

def findRoster(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT pokemon.name FROM pokemon join pokemon_owner on pokemon.id = pokemon_owner.pokemon_id join owner on owner.id=pokemon_owner.owner_id WHERE owner.name= '{}'".format(trainer_name)
            cursor.execute(query)
            result = []
            for c in cursor.fetchall():
                result.append(c["name"])
            return result
    except:
        print("DB Error")
print(get_haviest_pokemon())
print(findByType("grass"))
print(findOwners("gengar"))
print(findRoster("Loga"))
# insert_data(connection)