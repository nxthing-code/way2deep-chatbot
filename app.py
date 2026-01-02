import streamlit as st
import google.generativeai as genai
from PIL import Image
from typing import List
import numpy as np

# --- 1️⃣ Configuración de la página
st.set_page_config(page_title="Self-Discovery AI", page_icon="✨")
st.title("✨ Descubre tu Máximo Potencial (Embeddings)")

st.markdown("""
Analiza tus canciones favoritas mediante vectores para descubrir patrones o similitudes.
**Escribe tus canciones favoritas** o **sube una captura de pantalla** para analizar.
""")

# --- 2️⃣ Configurar API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.warning("⚠️ Añade tu API Key en Streamlit Secrets con la clave GOOGLE_API_KEY")
    st.stop()

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key, transport="rest")

# --- 3️⃣ Función para generar embeddings de texto
def get_embedding(texts: List[str]):
    embeddings = []
    for t in texts:
        emb_response = genai.embeddings.create(
            model="embedding-gecko-001",  # modelo gratuito
            input=t
        )
        embeddings.append(np.array(emb_response.data[0].embedding))
    return embeddings

# --- 4️⃣ Función para calcular similitud coseno
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# --- 5️⃣ Entrada del usuario
col1, col2 = st.columns([2, 1])
with col1:
    song_input = st.text_area("Escribe tus canciones favoritas, separadas por comas")
with col2:
    uploaded_file = st.file_uploader("Sube una captura 📸", type=["png", "jpg", "jpeg"])

# --- 6️⃣ Procesar datos
if song_input or uploaded_file:
    songs = [s.strip() for s in song_input.split(",") if s.strip()]
    if uploaded_file:
        st.info("Actualmente la imagen se puede subir, pero solo se procesan títulos de canciones por texto.")

    if songs:
        try:
            embeddings = get_embedding(songs)
            st.success("✅ Embeddings generados con éxito!")

            # Comparar similitud entre canciones
            st.subheader("Similitudes entre canciones")
            for i in range(len(songs)):
                for j in range(i+1, len(songs)):
                    sim = cosine_similarity(embeddings[i], embeddings[j])
                    st.write(f"**{songs[i]}** ↔ **{songs[j]}** → Similaridad: {sim:.2f}")

            # Recomendaciones simples: mostrar canción más “parecida” para cada una
            st.subheader("Recomendaciones basadas en similitud")
            for i, s in enumerate(songs):
                similarities = [cosine_similarity(embeddings[i], embeddings[j]) if i != j else -1 for j in range(len(songs))]
                if len(similarities) > 1:
                    best_idx = np.argmax(similarities)
                    st.write(f"Para **{s}**, canción más similar: **{songs[best_idx]}** (sim {similarities[best_idx]:.2f})")

        except Exception as e:
            st.error(f"Error generando embeddings: {e}")
