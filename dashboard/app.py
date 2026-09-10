import streamlit as st
import requests

st.set_page_config(page_title="Predicción de Churn", page_icon="🎯")
st.title("🎯 Predicción de Churn de Clientes")
st.markdown("Ingresa las métricas de un cliente para predecir su probabilidad de abandono, usando el modelo entrenado y desplegado como API.")

API_URL = "https://churn-prediction-api-t9pk.onrender.com/predict"

with st.form("formulario_cliente"):
    col1, col2 = st.columns(2)
    with col1:
        recency = st.number_input("Recencia (días desde última compra)", min_value=0, value=30)
        frequency = st.number_input("Frecuencia (número de pedidos)", min_value=1, value=5)
        monetary = st.number_input("Monetario (£ gastado total)", min_value=0.0, value=500.0)
        unique_products = st.number_input("Productos distintos comprados", min_value=1, value=20)
    with col2:
        avg_basket = st.number_input("Tamaño promedio del pedido (unidades)", min_value=0.0, value=10.0)
        tenure = st.number_input("Antigüedad como cliente (días)", min_value=0, value=200)
        avg_order_value = st.number_input("Valor promedio por pedido (£)", min_value=0.0, value=100.0)

    submitted = st.form_submit_button("Predecir")

if submitted:
    payload = {
        "Recency": recency, "Frequency": frequency, "Monetary": monetary,
        "UniqueProducts": unique_products, "AvgBasketSize": avg_basket,
        "Tenure": tenure, "AvgOrderValue": avg_order_value
    }

    with st.spinner("Consultando la API... (puede tardar hasta 1 minuto si estaba dormida)"):
        try:
            response = requests.post(API_URL, json=payload, timeout=90)
            response.raise_for_status()
            resultado = response.json()

            st.metric("Probabilidad de Churn", f"{resultado['probabilidad_churn']:.1%}")

            if resultado["prediccion"] == 1:
                st.error(f"⚠️ {resultado['interpretacion']}")
            else:
                st.success(f"✅ {resultado['interpretacion']}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error al conectar con la API: {e}")