"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, favourite_planets, favourite_characters, character, planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/characters', methods=['GET'])
def get_characters():

    characters = character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    
    return jsonify(all_planets), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):

    user1 = User.query.get(id)

    if user1:
        return jsonify(user1.serialize()), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):

    character1 = character.query.get(id)

    if character1:
        return jsonify(character1.serialize()), 200
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):

    planet1 = planet.query.get(id)

    if planet1:
        return jsonify(planet1.serialize()), 200
    else:
        return jsonify({"error": "Planet not found"}), 404

@app.route('/user/favourites/<int:id>', methods=['GET'])
def getUserFavourites(id):

    planets = favourite_planets.query.filter_by(user_id=id)
    all_planets = list(map(lambda x: x.serialize(), planets))
    if all_planets:
        return jsonify(all_planets), 200
    else:
        return jsonify({"error": "Planet not found"}), 404

@app.route('/user', methods=['POST'])
def create_user():

    request_body_user = request.get_json()
    
    new_user = User(first_name=request_body_user["first_name"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(request_body_user), 200

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):

    request_body_user = request.get_json()
    
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException('user not found', status_code=404)
    
    if "first_name" in request_body_user:
        user1.first_name = request_body_user["first_name"]
    if "email" in request_body_user:
        user1.email = request_body_user["email"]
    db.session.commit()
    
    return jsonify(request_body_user), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    user1 = User.query.get(id)
    if user1 is None:
        raise APIException('user not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    
    return jsonify("ok"), 200

@app.route('/favourite_characters', methods=['POST'])
def add_favourite_characters():

    request_body_user = request.get_json()
    character_id = request_body_user["character_id"]
    user_id = request_body_user["user_id"]

    record = favourite_characters.query.filter_by(user_id=user_id, character_id=character_id)
    all_fav_characters = list(map(lambda x: x.serialize(), record))

    if len(record.all()) == 0:
        record = favourite_characters(user_id=user_id, character_id=character_id)
        db.session.add(record)
        db.session.commit()
        return jsonify(request_body_user)
    return jsonify(all_fav_characters)

@app.route('/favourite_planets', methods=['POST'])
def add_favourite_planets():

    request_body_user = request.get_json()
    planet_id = request_body_user["planet_id"]
    user_id = request_body_user["user_id"]

    record = favourite_planets.query.filter_by(user_id=user_id, planet_id=planet_id)
    all_fav_planets = list(map(lambda x: x.serialize(), record))

    if len(record.all()) == 0:
        record = favourite_planets(user_id=user_id, planet_id=planet_id)
        db.session.add(record)
        db.session.commit()
        return jsonify(request_body_user)

    return jsonify(all_fav_planets), 200

@app.route('/favourite_characters/<int:characterId>', methods=['DELETE'])
def delete_favourite_characters(characterId):
    record = favourite_characters.query.filter_by(character_id=characterId).first()

    if record:
        print('a')
        db.session.delete(record)
        db.session.commit()
    return jsonify('ok'), 200

@app.route('/favourite_planets/<int:planetId>', methods=['DELETE'])
def delete_favourite_planets(planetId):
    record = favourite_planets.query.filter_by(planet_id=planetId).first()

    if record:
        print('a')
        db.session.delete(record)
        db.session.commit()
    return jsonify('ok'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

