
from flask import (
    Blueprint,
    jsonify
)

from .db import get_db

main = Blueprint("main", __name__)

@main.get("/")
def index():
    return "<h1>Esta es la pagina principal de la API de yeltic para el protipo de Sedena</h1>"


@main.get("/all-patients")
def get_all_patients():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient;")
    patients = cursor.fetchall()
    cursor.close()
    return jsonify(patients)

