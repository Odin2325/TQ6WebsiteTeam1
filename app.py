from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angebot = db.Column(db.String(100))
    datum = db.Column(db.String(20))
    personen = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(100))
    nachname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    telefonnummer = db.Column(db.String(20))
    passwort = db.Column(db.String(200))

class GewinnspielTeilnahme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefonnummer = db.Column(db.String(20), nullable=False)
    pizzen = db.Column(db.Text, nullable=False) 
    kosten = db.Column(db.String(20), nullable=False)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)