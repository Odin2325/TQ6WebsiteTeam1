from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Veranstaltung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String())
    beschreibung = db.Column(db.String())
    ort = db.Column(db.String())
    kategorie = db.Column(db.String())
    datum = db.Column(db.String())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/einreichen', methods=["GET", "POST"])
def einreichen():
    if request.method == "POST":
        veranstaltung = Veranstaltung(
            titel=request.form["titel"],
            beschreibung=request.form["beschreibung"],
            datum=request.form["datum"],
            ort=request.form["ort"],
            kategorie=request.form["kategorie"]
        )
        db.session.add(veranstaltung)
        db.session.commit()
    return render_template('einreichen.html')

with app.app_context():
    db.create_all()
app.run(debug=True)
