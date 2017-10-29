# server.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/datos4.db'
db = SQLAlchemy(app)


class Dato(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	token_sensor = db.Column(db.String(128))
	medicion = db.Column(db.String(4))
	time_created = db.Column(db.DateTime(timezone=True), default=func.now())

@app.route("/")
def server_info():
    return jsonify({
        "server": "My API"
    })

@app.route("/datos/", endpoint="medicion", methods=["POST"])
def new_dato():
    from flask import request
    json = request.get_json()
    token = json.get("token")
    _medicion = json.get("valor")
    new_dato = Dato()
    new_dato.token_sensor = token
    new_dato.medicion = _medicion
    new_dato.time_created = func.now()
    db.session.add(new_dato)
    db.session.commit()

    return jsonify({"id": new_dato.id}), 201

@app.route("/datos/", endpoint="lista_datos", methods=["GET"])
def lista_datos():
    datos = Dato.query.order_by(Dato.id).all()

    return jsonify({
        "items": [{"id": x.id, "token": x.token_sensor, "valor": x.medicion, "timestamp": x.time_created} for x in datos]
    })

if __name__ == "__main__":
    db.create_all() # Creamos todas las tablas de la base de datos
    app.run(port=3000, host="0.0.0.0")
