import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import os

os.environ["STREAMLIT_DISABLE_TELEMETRY"] = "1"
st.set_page_config(layout="wide")
st.title("🛩️ Planificador de Fumigación Aérea")

@st.cache_data(ttl=600)
def cargar_datos():
    lotes = pd.read_excel("data/datos_lotes.xlsx", sheet_name=0)
    aeronaves = pd.read_excel("data/datos_aeronaves.xlsx", sheet_name=0)
    columnas_esperadas = ["prioridad", "estado_infeccion"]
    for col in columnas_esperadas:
        if col not in lotes.columns:
            st.error(f'Falta la columna requerida en la hoja de Lotes: `{col}`')
            st.stop()
    return lotes, aeronaves

lotes, aeronaves = cargar_datos()
st.subheader("📋 Información general de los lotes")
st.dataframe(lotes)
st.subheader("✈️ Información de aeronaves")
st.dataframe(aeronaves)

st.subheader("🗺️ Mapa base")
m = folium.Map(location=[lotes["latitud"].mean(), lotes["longitud"].mean()], zoom_start=13)
for i, row in lotes.iterrows():
    folium.Marker([row["latitud"], row["longitud"]],
                  popup=f"Lote {row['id_lote']} - Prioridad {row['prioridad']}"
                  ).add_to(m)
st_folium(m, width=700, height=500)
