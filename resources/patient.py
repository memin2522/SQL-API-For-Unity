from flask import (
    jsonify, 
    request,
    Blueprint
)
from flask.views import MethodView
from prototipe_app.db import get_db


blp = Blueprint("Patients", __name__)

@blp.get("/patient/<string:patient_id>")
def get_patient(patient_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM patient WHERE id = %s;", (patient_id,))
        patient = cursor.fetchone()
        if patient is None:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify(patient)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@blp.delete("/patient/<string:patient_id>")    
def delete_patient(patient_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(f"DELETE FROM patient WHERE id = %s;", (patient_id,))
        db.commit()
        return jsonify({"message":"Item Deleted"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
            cursor.close()

@blp.put("/patient/<string:patient_id>")       
def update_patient(patient_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        data = request.get_json()
        allowed_fields = ['registration', 'firstName', 'lastName', 'dateOfBirth', 'militaryStatus', 'militaryRank']

        fields_and_values = []
        values = []

        for field, value in data.items():
            if field in allowed_fields:
                fields_and_values.append(f"{field} = %s")
                values.append(value)
                
        if not fields_and_values:
            return jsonify({"error": "No data provided to update"}), 400
        
        values.append(patient_id)

        query_set_part = ", ".join(fields_and_values)
        querySQL = f"UPDATE patient SET {query_set_part} WHERE id = %s;"
        cursor.execute(querySQL, values)
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Patient not found"}), 404
        
        return jsonify({"message": "Patient updated successfully"}), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@blp.get("/all-patients")
def get_all_patients():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient;")
    patients = cursor.fetchall()
    cursor.close()
    return jsonify(patients)

@blp.post("/add-patient")
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
