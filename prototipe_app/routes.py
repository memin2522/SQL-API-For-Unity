
from flask import (
    Blueprint,
    jsonify
)

from .db import get_db

main = Blueprint("main", __name__)

@main.get("/")
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient;")
    patients = cursor.fetchall()
    cursor.close()
    return jsonify(patients)

