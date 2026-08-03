from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from typing import List
import os

# Initialize FastAPI app
app = FastAPI(
    title="Diabetes Prediction API",
    description="API for predicting diabetes risk using logistic regression",
    version="1.0.0"
)

# Load the trained model
MODEL_PATH = "models/diabetes_logistic_model.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define input schema using the EXACT column names from training
class PredictionInput(BaseModel):
    number_of_times_pregnant: float
    plasma_glucose_concentration: float
    diastolic_blood_pressure: float
    triceps_skin_fold_thickness: float
    serum_insulin: float
    body_mass_index: float
    diabetes_pedigree_function: float
    age_years: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "number_of_times_pregnant": 2.0,
                "plasma_glucose_concentration": 120.0,
                "diastolic_blood_pressure": 70.0,
                "triceps_skin_fold_thickness": 25.0,
                "serum_insulin": 80.0,
                "body_mass_index": 25.5,
                "diabetes_pedigree_function": 0.5,
                "age_years": 30.0
            }
        }

# Define output schema
class PredictionOutput(BaseModel):
    prediction: int  # 0 or 1
    probability: float  # probability of diabetes (class 1)
    risk_level: str  # "Low", "Medium", or "High"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Diabetes Prediction API is running!",
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model": "loaded"}

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """Make a prediction for diabetes risk"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert input to DataFrame with the EXACT column names from training
        input_dict = {
            "Number of times pregnant": input_data.number_of_times_pregnant,
            "Plasma glucose concentration a 2 hours in an oral glucose tolerance test": input_data.plasma_glucose_concentration,
            "Diastolic blood pressure (mm Hg)": input_data.diastolic_blood_pressure,
            "Triceps skin fold thickness (mm)": input_data.triceps_skin_fold_thickness,
            "2-Hour serum insulin (mu U/ml)": input_data.serum_insulin,
            "Body mass index (weight in kg/(height in m)^2)": input_data.body_mass_index,
            "Diabetes pedigree function": input_data.diabetes_pedigree_function,
            "Age (years)": input_data.age_years
        }
        
        input_df = pd.DataFrame([input_dict])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]  # probability of class 1 (diabetes)
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        return PredictionOutput(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict-batch")
async def predict_batch(input_data: List[PredictionInput]):
    """Make predictions for multiple inputs"""
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert list of inputs to DataFrame with correct column names
        input_dicts = []
        for item in input_data:
            input_dict = {
                "Number of times pregnant": item.number_of_times_pregnant,
                "Plasma glucose concentration a 2 hours in an oral glucose tolerance test": item.plasma_glucose_concentration,
                "Diastolic blood pressure (mm Hg)": item.diastolic_blood_pressure,
                "Triceps skin fold thickness (mm)": item.triceps_skin_fold_thickness,
                "2-Hour serum insulin (mu U/ml)": item.serum_insulin,
                "Body mass index (weight in kg/(height in m)^2)": item.body_mass_index,
                "Diabetes pedigree function": item.diabetes_pedigree_function,
                "Age (years)": item.age_years
            }
            input_dicts.append(input_dict)
        
        input_df = pd.DataFrame(input_dicts)
        
        # Make predictions
        predictions = model.predict(input_df)
        probabilities = model.predict_proba(input_df)[:, 1]
        
        # Prepare results
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            if prob < 0.3:
                risk_level = "Low"
            elif prob < 0.7:
                risk_level = "Medium"
            else:
                risk_level = "High"
                
            results.append({
                "prediction": int(pred),
                "probability": float(prob),
                "risk_level": risk_level
            })
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "feature_names": [
            "Number of times pregnant",
            "Plasma glucose concentration a 2 hours in an oral glucose tolerance test",
            "Diastolic blood pressure (mm Hg)",
            "Triceps skin fold thickness (mm)",
            "2-Hour serum insulin (mu U/ml)",
            "Body mass index (weight in kg/(height in m)^2)",
            "Diabetes pedigree function",
            "Age (years)"
        ],
        "n_features": 8,
        "classes": [0, 1],
        "class_labels": ["No Diabetes", "Diabetes"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)