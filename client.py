from database import db

class Client(db.Model):

    __tablename__ = "clients"
    
    client_id = db.Column(db.Integer, nullable= False, primary_key= True)
    name = db.Column(db.String(50), nullable= False, unique= True)
    age = db.Column(db.Integer, nullable= False)
    weight = db.Column(db.Float, nullable= False)
    email = db.Column(db.String(80), nullable= False, unique= True)
    active = db.Column(db.Boolean, nullable= False)