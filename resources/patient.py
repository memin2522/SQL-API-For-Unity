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

        query = ""
        for field, value in data.items():
            if field in allowed_fields:
                query.append(f"{field} = {value},")
            
        if query == "":
            return jsonify({"error": "No data provided to update"}), 400
        
        querySQL =f"UPDATE patient SET {query} WHERE id = %s", (patient_id,)
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
