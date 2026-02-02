from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db
from client import Client

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/daily_diet'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def database_app_info():
    with app.app_context():
        db.create_all()

@app.route("/client", methods=['POST'])
def create_user():
    client_data = request.get_json()

    client_name = client_data.get("name")
    client_age = client_data.get("age")
    client_weight = client_data.get("weight")
    client_email = client_data.get("email")
    client_active = client_data.get("active")

    new_client = Client(name= client_name, 
                        age= client_age, 
                        weight= client_weight, 
                        email= client_email, 
                        active= client_active)

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "created user"}), 200

if __name__ == "__main__":
    database_app_info()
    app.run(debug=True)

