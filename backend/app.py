import json
import redis
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from scrappy import scrapgoogle

app = Flask(__name__)
CORS(app)

cache = redis.Redis(host='redis', port=6379)
config = {
    'user': 'local_user',
    'password': 'root12345',
    'host': 'db',
    'port': '3306',
    'database': 'local_database'
}
connection = mysql.connector.connect(**config)

@app.route('/')
def status():
    return jsonify(
        message="Congratulation! API is working properly."
    ), 200

@app.route('/search', methods=['GET'])
def search():
    if request.values.get('search_term') is None:
        return jsonify(
            message="Parameter search_term is required for this API."
        ), 422

    cursor = connection.cursor()

    try:
        search_term = request.values.get('search_term')
        key = search_term.lower().replace(' ', '_')
        recipes = cache.get(key)
        
        if recipes is None:
            response = scrapgoogle(search_term)
            cache[key] = json.dumps(response.__dict__)

            sql = "INSERT INTO recipes_popularity (recipe_key, total_hit) VALUES (%s, %s)"
            val = (key, 1)
            cursor.execute(sql, val)

            connection.commit()
            cursor.close()

            return jsonify(
                ingredients=response.ingredients,
                serving=response.serving,
                image=response.image,
                directions=response.directions
            ), 200
        else:
            cursor.execute('SELECT * FROM recipes_popularity WHERE recipe_key = \'' + key + '\'')
            results = [[id, total_hit] for (id, recipe_key, total_hit) in cursor]

            sql = "UPDATE recipes_popularity SET total_hit=%s WHERE id=%s"
            val = (results[0][1] + 1, results[0][0])
            cursor.execute(sql, val)

            connection.commit()
            cursor.close()

            return jsonify(json.loads(recipes)), 200
    except redis.exceptions.ConnectionError as exc:
        return jsonify(
            error="Redis database is down!"
        ), 503

@app.route('/top-recipes', methods=['GET'])
def topRecipes():
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM recipes_popularity ORDER BY total_hit DESC LIMIT 3')
    results = [[recipe_key, total_hit] for (id, recipe_key, total_hit) in cursor]
    cursor.close()

    recipes = []
    for x in results:
        recipe = cache.get(x[0])
        recipe = json.loads(recipe)
        recipe['key'] = x[0]
        recipe['total_hits'] = x[1]
        recipes.append(recipe)

    return jsonify(recipes), 200