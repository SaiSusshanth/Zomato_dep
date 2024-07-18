from flask import Flask, request, jsonify
from pymongo import MongoClient
from math import ceil
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# MongoDB configuration
client = MongoClient('localhost', 27017)
db = client['zomato_db']
collection = db['restaurants']
# print(type(collection))
TOTAL_ENTRIES = collection.count_documents({})
PAGE_LIMIT = 10


@app.route('/restaurant/<int:id>', methods=['GET'])
def get_restaurant(id):
    try:
        restaurant = collection.find_one({'Restaurant ID': id})
        if restaurant:
            restaurant['_id'] = str(restaurant['_id'])
            return jsonify(restaurant)
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/country', methods=['GET'])
def get_restaurant_by_Country():
    try:
        page = int(request.args.get('page', 1))
        per_page = PAGE_LIMIT
        country = (request.args.get('country', ''))
        skips = per_page * (page - 1)

        restaurants = list(collection.find({'Country': country}).skip(skips).limit(per_page))
        
        total = len(restaurants)
        total_pages = ceil(total / per_page)

        if page > total_pages or page < 1:
            return jsonify({
                "error": "Page out of range",
                "total_pages": total_pages
            }), 400
        
        print(country, type(country))
        if restaurants:
            for i in restaurants:
                i["_id"] = str(i['_id'])
            
            return jsonify({
            "restaurants": restaurants,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
            })
            # return jsonify(restaurants)
        else:
            return jsonify({"error": "No Restaurant found"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        page = int(request.args.get('page', 1))
        # per_page = int(request.args.get('per_page', 10))
        per_page = PAGE_LIMIT

        # total = collection.count_documents({})
        total = TOTAL_ENTRIES
        total_pages = ceil(total / per_page)

        if page > total_pages or page < 1:
            return jsonify({
                "error": "Page out of range",
                "total_pages": total_pages
            }), 400

        skips = per_page * (page - 1)
        restaurants = list(collection.find().skip(skips).limit(per_page))
        for restaurant in restaurants:
            restaurant['_id'] = str(restaurant['_id'])

        return jsonify({
            "restaurants": restaurants,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/')
def index():
    return 'PlaceHolder for now'

app.run(host = '0.0.0.0', port = 80)

