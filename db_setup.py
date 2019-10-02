from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.sqlite3'

db = SQLAlchemy(app)
class Pets(db.Model):
	id = db.Column('pet_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	age = db.Column(db.Integer)  
	sex = db.Column(db.String(200))
	description = db.Column(db.String(500))

db.create_all()   