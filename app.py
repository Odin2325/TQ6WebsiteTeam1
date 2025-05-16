from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from markupsafe import escape
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

kategorien = [
    'Party',
    'Konzert',
    'Festival',
    'Filmabend',
    'Karaoke'
]

class Veranstaltung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String())
    beschreibung = db.Column(db.String())
    ort = db.Column(db.String())
    kategorie = db.Column(db.String())
    datum = db.Column(db.String())
    counter = db.Column(db.Integer)

@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    veranstaltung = Veranstaltung.query.get_or_404(id)
    veranstaltung.counter = veranstaltung.counter + 1
    db.session.commit()
    return jsonify({'new_count': veranstaltung.counter})

@app.route('/')
def index():
    datum = request.args.get('datum', str(date.today()))

    selected = request.args.getlist('kategorie')
    if selected == []: selected = kategorien

    veranstaltungen = Veranstaltung.query.filter(
            Veranstaltung.datum >= datum,
            Veranstaltung.kategorie.in_(selected)).order_by(Veranstaltung.datum).all()

    return render_template(
        'index.html',
        veranstaltungen=veranstaltungen,
        datum=datum,
        kategorien=kategorien,
        selected=selected)

@app.route('/detail/<int:id>')
def detail(id):
    veranstaltung = Veranstaltung.query.filter(
        Veranstaltung.id == id).first()
    db.session.commit()
    return render_template('detail.html', veranstaltung=veranstaltung)

@app.route('/einreichen', methods=['GET', 'POST'])
def einreichen():
    if request.method == 'POST':
        beschreibung = request.form['beschreibung']
        beschreibung = str(escape(beschreibung))
        beschreibung = beschreibung.replace('\r\n','<br>')

        veranstaltung = Veranstaltung(
            titel=request.form['titel'],
            beschreibung=beschreibung,
            datum=request.form['datum'],
            ort=request.form['ort'],
            kategorie=request.form['kategorie'],
            counter=0
        )
        db.session.add(veranstaltung)
        db.session.commit()
        return redirect('/')
    return render_template('einreichen.html', kategorien=kategorien)

with app.app_context():
    db.create_all()
app.run(debug=True)
