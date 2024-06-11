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
def put_patient(patient_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        data = request.get_json()
        allowed_fields = ['registration', 'firstName', 'lastName', 'dateOfBirth', 'militaryStatus', 'militaryRank']

        fields_and_values = []
        for field, value in data.items():
            if field in allowed_fields:
                fields_and_values.append((f"{field} = '{value}'")) 
                
        if fields_and_values is None:
            return jsonify({"error": "No data provided to update"}), 400
        
        query_set_part = ", ".join(fields_and_values)
        querySQL =f"UPDATE patient SET {query_set_part} WHERE id = {patient_id};"
        return querySQL
        cursor.execute(querySQL) 
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Patient not found"}), 404
            
        return jsonify({"error": "No data provided to update"}), 400
        
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
