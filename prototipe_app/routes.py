
from flask import (
    Blueprint,
    jsonify, 
    request
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

@main.post("/add-patient")
def add_patient():
    data = request.get_json()
    required_fields = ['registration', 'firstName', 'lastName', 'dateOfBirth', 'militaryStatus', 'militaryRank']

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"El campo {field} es requerido"
            }), 400

    registration = data['registration']
    firstName = data['firstName']
    lastName = data['lastName']
    dateOfBirth = data['dateOfBirth']
    militaryStatus = data['militaryStatus']
    militaryRank = data['militaryRank']

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO patient (registration, firstName, lastName, dateOfBirth, militaryStatus, militaryRank)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (registration, firstName, lastName, dateOfBirth, militaryStatus, militaryRank))
        db.commit()
        current_id = cursor.lastrowid
        cursor.close()
        return jsonify({
            "id": current_id,
            "registration": registration,
            "firstName": firstName,
            "lastName": lastName,
            "dateOfBirth": dateOfBirth,
            "militaryStatus": militaryStatus,
            "militaryRank": militaryRank
        }), 201
    except Exception as e:
        db.rollback()
        cursor.close()
        return jsonify({
            "error": str(e)
        }), 500
