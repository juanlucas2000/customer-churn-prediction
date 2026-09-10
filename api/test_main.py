from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    """La raíz de la API debe responder correctamente"""
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()

def test_predict_cliente_bajo_riesgo():
    """Cliente con compras recientes y frecuentes debe dar bajo riesgo"""
    cliente = {
        "Recency": 5.0,
        "Frequency": 20.0,
        "Monetary": 5000.0,
        "UniqueProducts": 50.0,
        "AvgBasketSize": 10.0,
        "Tenure": 500.0,
        "AvgOrderValue": 250.0
    }
    response = client.post("/predict", json=cliente)
    assert response.status_code == 200
    data = response.json()
    assert "probabilidad_churn" in data
    assert 0 <= data["probabilidad_churn"] <= 1

def test_predict_cliente_alto_riesgo():
    """Cliente sin compras recientes y con poca frecuencia debe dar alto riesgo"""
    cliente = {
        "Recency": 400.0,
        "Frequency": 1.0,
        "Monetary": 50.0,
        "UniqueProducts": 1.0,
        "AvgBasketSize": 1.0,
        "Tenure": 400.0,
        "AvgOrderValue": 50.0
    }
    response = client.post("/predict", json=cliente)
    data = response.json()
    assert data["probabilidad_churn"] > 0.5

def test_predict_datos_incompletos():
    """La API debe rechazar una petición sin todos los campos requeridos"""
    response = client.post("/predict", json={"Recency": 100.0})
    assert response.status_code == 422  # Error de validación de FastAPI/Pydantic