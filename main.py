from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import pandas as pd
import numpy as np
import os

# Load the trained model from MLflow (replace with your model's path if necessary)
MODEL_URI = "models:/tracking_forest_fire_prediction_model/latest"
model = mlflow.pyfunc.load_model(MODEL_URI)

# Initialize FastAPI app
app = FastAPI()

# Define request data structure
class PredictionRequest(BaseModel):
    X: float
    Y: float
    month: float
    day: float
    FFMC: float
    DMC: float
    DC: float
    ISI: float
    temp: float
    RH: float
    wind: float
    rain: float

# Define response data structure
class PredictionResponse(BaseModel):
    prediction: float

@app.get("/")
def read_root():
    return {"message": "Forest Fire Prediction API"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    # Convert input data to a DataFrame
    input_data = pd.DataFrame([data.dict()])
    
    # Make a prediction
    try:
        prediction = model.predict(input_data)
        return PredictionResponse(prediction=prediction[0][0])  # Assuming single output regression
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

