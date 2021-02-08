from flask import Flask, request, Response, jsonify
import model
import json


app = Flask(__name__)


# @app.route('/pokemons/name/<pokemon_name>')  # the DB is updated with each call
def update_types_and_get_pokemon(pokemon_name):
    pokemon_dict = model.update_types_and_get_pokemon_by_name(pokemon_name)
    if type(pokemon_dict) is int:
        if pokemon_dict == 404:
            return Response("There is no such pokemon."), 404
        elif pokemon_dict == 500:
            return Response("The DB failed on request."), 500

    return jsonify(pokemon_dict)


def get_pokemons_by_trainer():
    try:
        trainer_name = request.args.get("trainer")
        results = model.get_pokemons_by_trainer(trainer_name)
        res = Response((json.dumps(results)))
        code = 200
    except Exception as e:
        res = Response(json.dumps({"Error": str(e)}))
        code = 400
    res.headers["Content-Type"] = "application/json"
    return res, code


@app.route('/pokemons/type/<type_>')
def get_pokemons_by_type(type_):
    return None


@app.route('/pokemons')
def get_pokemon_by_filters():
    param_dict = request.args
    if "name" in param_dict:
        return update_types_and_get_pokemon(param_dict["name"])
    elif "trainer" in param_dict:
        return get_pokemons_by_trainer(param_dict["trainer"])
    elif "type" in param_dict:
        return get_pokemons_by_type(param_dict["type"])
    else:
        return jsonify({"Error": "The format of the request is incorrect: either \'trainer\' "
                                 "or \'name\' or \'type\' should be query parameters."}), 400


@app.route('/trainers', methods=["POST"])
def create_new_trainer():
    try:
        data = request.get_json()
        model.add_trainer(data.get("name"), data.get("town"))
    except Exception as e:
        return jsonify({"Error": str(e)})

    return Response("Success - Added trainer")


@app.route('/trainers')
def get_trainers_of_pokemon():
    pokemon_name = request.args.get("pokemon")
    try:
        results = model.get_trainers_of_pokemon(pokemon_name)
        res = Response((json.dumps(results)))
    except Exception as e:
        res = Response(json.dumps({"Error": str(e)}))
    res.headers["Content-Type"] = "application/json"
    return res


@app.route('/pokemons?pokemon=<pokemon_name>&trainer=<trainer_name>', methods=["DELETE"])
def delete_pokemon_from_trainer(pokemon_name, trainer_name):
    pass


@app.route('/pokemons/evolve', methods=["PUT"])
def evolve_pokemon():
    pokemon_trainer_dict = request.get_json()
    if not pokemon_trainer_dict.get("trainer") or not pokemon_trainer_dict.get("pokemon"):
        return jsonify({"Error": "The format of the request is incorrect: should be a json of dict "
                                 "form with \'trainer\' and \'pokemon\' as keys"}), 400

    trainer_name = pokemon_trainer_dict["trainer"]
    pokemon_name = pokemon_trainer_dict["pokemon"]
    code = model.evolve_pokemon_of_trainer(pokemon_name, trainer_name)
    code_dict = {1: {"Error": "The pokemon cannot evolve any more"},
                 2: {"Error": "The pokemon does not appear in our DB"},
                 3: {"Error": "The evolved pokemon does not appear in our DB"},
                 4: {"Error": "This trainer does not appear in our DB"},
                 5: {"Error": "This trainer doesn't hold a pokemon of this species"}}
    if type(code) is str:
        return jsonify({"updated": {"trainer": trainer_name, "evolved pokemon": code}})
    elif 1 <= code <= 5:
        return jsonify(code_dict[code]), 404
    else:
        return jsonify({"Error": "The DB failed on request."}), 500


if __name__ == '__main__':
    app.run(port=3000)
