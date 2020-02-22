import json
import redis

from flask import Flask, jsonify, request
from flask_cors import CORS
from scrappy import scrapgoogle

app = Flask(__name__)
CORS(app)

cache = redis.Redis(host='redis', port=6379)

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
    
    try:
        search_term = request.values.get('search_term')
        key = search_term.lower().replace(' ', '_')
        recipes = cache.get(key)
        
        if recipes is None:
            response = scrapgoogle(search_term)
            cache[key] = json.dumps(response.__dict__)

            return jsonify(
                ingredients=response.ingredients,
                serving=response.serving,
                image=response.image,
                directions=response.directions
            ), 200
        else:
            return jsonify(json.loads(recipes)), 200
    except redis.exceptions.ConnectionError as exc:
        return jsonify(
            error="Redis database is down!"
        ), 503
