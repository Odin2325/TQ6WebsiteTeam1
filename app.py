from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

kategorien = [
    "Party",
    "Konzert",
    "Festival",
    "Filmabend",
    "Karaoke"
]

class Veranstaltung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String())
    beschreibung = db.Column(db.String())
    ort = db.Column(db.String())
    kategorie = db.Column(db.String())
    datum = db.Column(db.String())

@app.route('/')
def index():
    datum = request.args.get('datum', str(date.today()))
    kategorie = request.args.get('kategorie', 'Party')

    veranstaltungen = Veranstaltung.query.filter(
        Veranstaltung.datum >= datum,
        Veranstaltung.kategorie == kategorie).all()
    
    return render_template(
        'index.html',
        veranstaltungen=veranstaltungen,
        datum=datum,
        kategorien=kategorien,
        selected=kategorie)

@app.route('/detail/<int:id>')
def detail(id):
    veranstaltung = Veranstaltung.query.filter(
        Veranstaltung.id == id).first()
    return render_template('detail.html', veranstaltung=veranstaltung)

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
    return render_template('einreichen.html', kategorien=kategorien)

with app.app_context():
    db.create_all()
app.run(debug=True)
