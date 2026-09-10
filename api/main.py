from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="API de Predicción de Churn")

modelo = joblib.load('model/modelo_churn.pkl')
scaler = joblib.load('model/scaler.pkl')

COLUMNAS = ['Recency', 'Frequency', 'Monetary', 'UniqueProducts',
            'AvgBasketSize', 'Tenure', 'AvgOrderValue']

class ClienteFeatures(BaseModel):
    Recency: float
    Frequency: float
    Monetary: float
    UniqueProducts: float
    AvgBasketSize: float
    Tenure: float
    AvgOrderValue: float

@app.get("/")
def home():
    return {"mensaje": "API de predicción de churn activa. Ve a /docs para probarla."}

@app.post("/predict")
def predecir_churn(cliente: ClienteFeatures):
    datos = pd.DataFrame([cliente.model_dump()])[COLUMNAS]
    datos_escalados = scaler.transform(datos)

    probabilidad = modelo.predict_proba(datos_escalados)[0][1]
    prediccion = int(modelo.predict(datos_escalados)[0])

    return {
        "prediccion": prediccion,
        "probabilidad_churn": round(float(probabilidad), 4),
        "interpretacion": "Alto riesgo de churn" if probabilidad >= 0.5 else "Bajo riesgo de churn"
    }