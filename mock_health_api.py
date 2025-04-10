from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Mock medication data
medications = {
    "paracetamol": {
        "usage": "Used to treat pain and fever.",
        "dosage": "500mg every 4–6 hours (not more than 4g/day)"
    },
    "metformin": {
        "usage": "Used to control blood sugar levels in Type 2 diabetes.",
        "dosage": "500–1000mg twice daily with meals."
    }
}

# Normal health metric ranges
normal_ranges = {
    "heart_rate": "60-100 bpm",
    "blood_pressure": "90/60 mmHg to 120/80 mmHg",
    "glucose": "70-99 mg/dL (fasting)"
}


@app.get("/medication_info")
def get_medication_info(name: str):
    data = medications.get(name.lower())
    if not data:
        return JSONResponse(content={"error": "Medication not found"}, status_code=404)
    return data


@app.get("/normal_ranges")
def get_normal_ranges(metric: str):
    data = normal_ranges.get(metric.lower())
    if not data:
        return JSONResponse(content={"error": "Metric not found"}, status_code=404)
    return {"metric": metric, "normal_range": data}
