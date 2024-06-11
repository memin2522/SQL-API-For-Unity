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

        fields_query = []
        values = []

        for field, value in data.items():
            if field in allowed_fields:
                fields_query.append(f"{field} = %s")
                values.append(value)
            
        if not fields_query:
            return jsonify({"error": "No data provided to update"}), 400
            
        values.append(patient_id)

        query =f"UPDATE patient SET {', '.join(fields_query)} WHERE id = %s", (patient_id,)
        cursor.execute(query,values) 
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Patient not found"}), 404
            
        return jsonify({"error": "No data provided to update"}), 400
        
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
