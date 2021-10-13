from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app_aula2 = Flask(__name__)
app_aula2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db=SQLAlchemy(app_aula2)

class Parent (db.Model):
    id = db.Column (db.Integer, primary_key= True)
    name = db.Column (db.String (500))
    child = db.relationship ('Child', backref='parent', uselist =False)

class Child (db.Model):
    id = db.Column (db.Integer, primary_key= True)
    name = db.Column (db.String (500))
    parent_id =db.Column (db.Integer, db.ForeignKey ('parent.id'), unique =True)

app_aula2.run (debug=True)