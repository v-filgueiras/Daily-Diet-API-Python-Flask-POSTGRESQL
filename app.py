from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db
from client import Client
from meal import Meal
from datetime import datetime
import psycopg2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/daily_diet'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def database_app_info():
    with app.app_context():
        db.drop_all()
        db.create_all()

@app.route("/client", methods=['POST'])
def create_user():
    client_data = request.get_json()

    client_name = client_data.get("name")
    client_age = client_data.get("age")
    client_weight = client_data.get("weight")
    client_email = client_data.get("email")
    client_active = client_data.get("active", True)

    new_client = Client(
        name=client_name, 
        age=client_age, 
        weight=client_weight,
        email=client_email, 
        active=client_active
    )
    
    fields_required = ["name", "age", "weight", "email"]

    for field in fields_required:
        if field not in client_data or client_data[field] is None:
            return jsonify({"message": f"{field} is required"}), 400

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "created user"}), 200

@app.route("/clients", methods=['GET'])
def get_clients():
    clients = Client.query.all()

    clients_list = []
    for client in clients:
        clients_list.append({
            "id": client.client_id,
            "name": client.name,
            "age": client.age,
            "weight": client.weight,
            "email": client.email,
            "active": client.active
        })

    return jsonify({"clients": clients_list}), 200

@app.route("/client/<int:client_id>", methods=['GET'])
def get_client(client_id):
    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({"message": "Client not found"}), 404

    return jsonify({
        "client_id": client.client_id,
        "name": client.name,
        "age": client.age,
        "weight": client.weight,
        "email": client.email,
        "active": client.active
    }), 200

@app.route("/client/<int:client_id>", methods=['DELETE'])
def delete_client(client_id):
    client = db.session.get(Client, client_id)

    if not client:
        return jsonify({"message": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()

    return jsonify({
        "message": "succesfull client deleted",
        "name": client.name
    }), 200

@app.route("/meal", methods=['POST'])
def create_meal():
    meal_data = request.get_json()

    name = meal_data.get("name")
    description = meal_data.get("description")
    total_calories = meal_data.get("total_calories")

    new_meal = Meal(name= name,
                    description= description,
                    date_time = datetime.now(),
                    total_calories= total_calories)
    
    required_fields = ["name", "total_calories"]

    for field in required_fields:
        if field not in meal_data or meal_data[field] is None:
            return jsonify({"message": f"{field} is required"}), 400

    db.session.add(new_meal)
    db.session.commit()

    return jsonify({"message": "created meal"}), 200


if __name__ == "__main__":
    database_app_info()
    app.run(debug=True)
