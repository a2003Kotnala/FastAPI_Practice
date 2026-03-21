from fastapi import FastAPI, Path, HTTPException,Query
import json

app = FastAPI()

def load_patient_data():
    with open("patient_data.json", "r") as f:
        patient_data = json.load(f)
    return patient_data


@app.get("/")
def hello():
    return {"message": "Hello, patient!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}

@app.get("/view")
def view():
    data = load_patient_data()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve" )):
    data = load_patient_data()
    if patient_id not in data:
        return {"error": "Patient not found"}
    else:
        return {patient_id: data[patient_id]}


@app.get("/patient/{patient_id}/age")
def view_patient_age(patient_id: str=Path(..., description="The ID of the patient to retrieve age for"  )):
    data = load_patient_data()
    if patient_id not in data:
        return {"error": "Patient not found"}
    else:
        return {"age": data[patient_id]["age"]}
    
@app.delete("/patient/{patient_id}")
def delete_patient(patient_id: str):
    data = load_patient_data()
    if patient_id not in data:
        return {"error": "Patient not found"}
    else:
        del data[patient_id]
        with open("patient_data.json", "w") as f:
            json.dump(data, f)
        return {"message": "Patient deleted successfully"}
    
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients")):
    data = load_patient_data()
    if sort_by not in ["age", "name"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    sorted_patients = sorted(data.items(), key=lambda x: x[1][sort_by])
    return {patient_id: patient_info for patient_id, patient_info in sorted_patients}